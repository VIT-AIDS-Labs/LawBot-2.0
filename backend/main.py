# backend/main.py
"""
LawBot 2.0 — AI-Powered Legal Assistance Backend
Unified FastAPI server with all modules.
"""
print("=== LawBot 2.0 main.py (unified backend) ===")

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from pathlib import Path
from threading import Lock
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

# Import modules
from backend.legal_sections import get_section_info
from backend.document_analysis import extract_text_from_pdf, analyze_document
from backend.lawyer_connect import (
    get_lawyers as db_get_lawyers,
    get_lawyer_by_id,
    create_consultation_request,
    get_consultation_requests,
    get_filter_options,
)
from backend.evaluation import get_evaluation_data
from backend.database import init_db

# ---------------------------------------
# LLM CLIENT
# ---------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if GEMINI_API_KEY:
    openai_client = OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.6-flash")
else:
    openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# ---------------------------------------
# PATH CONFIG
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent
DATA_DIR = MODEL_PATH / "data"
FRONTEND_DIR = MODEL_PATH / "frontend"

TOP_K = 5
MIN_RELEVANCE_SCORE = 0.65

EMB_PATH = DATA_DIR / "section_embs.npy"
ID_PATH = DATA_DIR / "section_ids.txt"
CSV_PATH = DATA_DIR / "sections_clean.csv"

# ---------------------------------------
# APP SETUP
# ---------------------------------------

app = FastAPI(title="LawBot 2.0 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files will be mounted at the end to avoid overriding API routes


# ---------------------------------------
# REQUEST / RESPONSE MODELS
# ---------------------------------------

class QueryIn(BaseModel):
    query: str | None = None
    text: str | None = None


class LegalQueryIn(BaseModel):
    query: str


class ConsultationIn(BaseModel):
    name: str
    legal_issue: str
    preferred_language: str | None = None
    preferred_date: str | None = None
    contact_info: str
    description: str | None = None
    lawyer_id: int | None = None


# ---------------------------------------
# GLOBAL STATE
# ---------------------------------------

MODEL: SentenceTransformer | None = None
SECTIONS_DF: pd.DataFrame | None = None
SECTION_EMBS: np.ndarray | None = None
SECTION_IDS: list[str] | None = None

_EMB_LOCK = Lock()


# ---------------------------------------
# UTILS (preserved from original)
# ---------------------------------------

def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return np.dot(b_norm, a_norm)


def score_to_confidence(score: float) -> str:
    if score >= 0.85:
        return "High"
    if score >= 0.65:
        return "Medium"
    return "Low"


def build_sections_from_excels() -> pd.DataFrame:
    excel_files = [
        DATA_DIR / "train_1.xlsx",
        DATA_DIR / "train_2.xlsx",
        DATA_DIR / "train_3.xlsx",
        DATA_DIR / "train_4.xlsx",
        DATA_DIR / "train_5.xlsx",
    ]

    dfs = []
    for path in excel_files:
        if not path.exists():
            print(f"[build_sections] Missing: {path}")
            continue

        print(f"[build_sections] Reading (no header): {path}")
        df_raw = pd.read_excel(path, header=None)
        if df_raw.empty:
            print(f"[build_sections] Empty file: {path}")
            continue

        n_cols = df_raw.shape[1]
        if n_cols < 2:
            raise RuntimeError(f"{path} has fewer than 2 columns")

        section_idx = n_cols - 1
        text_idx = n_cols - 2
        df = df_raw[[section_idx, text_idx]].rename(
            columns={section_idx: "section", text_idx: "text"}
        )
        dfs.append(df)

    if not dfs:
        raise RuntimeError("No valid train_*.xlsx files found in data/.")

    sections_df = pd.concat(dfs, ignore_index=True)
    sections_df["text"] = sections_df["text"].fillna("").astype(str)
    sections_df["section"] = sections_df["section"].astype(str)
    sections_df = sections_df[sections_df["text"].str.strip() != ""]

    print(f"[build_sections] Final merged shape: {sections_df.shape}")
    return sections_df


def ensure_embeddings_ready():
    """Lazy initializer for SECTION_EMBS and SECTION_IDS."""
    global SECTION_EMBS, SECTION_IDS, SECTIONS_DF, MODEL

    if SECTION_EMBS is not None and SECTION_IDS is not None:
        return

    with _EMB_LOCK:
        if SECTION_EMBS is not None and SECTION_IDS is not None:
            return
        if SECTIONS_DF is None:
            raise RuntimeError("SECTIONS_DF is None inside ensure_embeddings_ready.")

        texts = SECTIONS_DF["text"].tolist()
        print(f"[emb] Computing embeddings for {len(texts)} texts (first time)...")

        SECTION_EMBS = MODEL.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=False,
        )
        SECTION_IDS = SECTIONS_DF["section"].tolist()

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            print("[emb] Saving embedding cache to disk...")
            np.save(EMB_PATH, SECTION_EMBS)
            with open(ID_PATH, "w", encoding="utf-8") as f:
                for sid in SECTION_IDS:
                    f.write(str(sid) + "\n")
            print(f"[emb] Saved cache for {len(SECTION_IDS)} rows.")
        except Exception as e:
            print("[emb] WARNING: Failed to save cache:", e)

        print("[emb] Embedding computation finished.")


def retrieve_top_k(query: str, k: int = TOP_K) -> list[dict]:
    """
    Use our fine-tuned LegalBERT to retrieve top-k relevant *unique* sections.
    Deduplicates by section code — keeps only the highest-scoring match per section.
    Returns list of dicts with section info, text, score, confidence.
    """
    ensure_embeddings_ready()

    query_emb = MODEL.encode([query], convert_to_numpy=True)[0]
    sims = cosine_sim(query_emb, SECTION_EMBS)

    # Sort ALL indices by descending similarity
    sorted_idx = np.argsort(-sims)

    results = []
    seen_sections = set()

    for idx in sorted_idx:
        score = float(sims[idx])
        if score < MIN_RELEVANCE_SCORE:
            break  # All remaining scores are lower, so stop

        sec_code = SECTION_IDS[idx]

        # Skip if we already have this section
        if sec_code in seen_sections:
            continue
        seen_sections.add(sec_code)

        sec_text = SECTIONS_DF.iloc[idx]["text"]
        sec_info = get_section_info(sec_code)

        result = {
            "section_code": sec_code,
            "score": round(score, 6),
            "confidence": score_to_confidence(score),
            "text": sec_text,
        }

        if sec_info:
            result["act"] = sec_info["act"]
            result["section"] = sec_info["section"]
            result["title"] = sec_info["title"]
            result["legal_text"] = sec_info.get("legal_text")
        else:
            result["act"] = "Indian Penal Code"
            result["section"] = sec_code
            result["title"] = None
            result["legal_text"] = None

        results.append(result)

        if len(results) >= k:
            break

    return results


# ---------------------------------------
# RAG: Generate legal explanation
# ---------------------------------------

def generate_rag_explanation(query: str, references: list[dict]) -> str:
    """
    RAG pipeline: use retrieved legal sections as context for Gemini.
    """
    if openai_client is None:
        return (
            "Explanation service is not configured. "
            "Please set the GEMINI_API_KEY environment variable."
        )

    if not references:
        return (
            "No sufficiently relevant legal provisions were found for your query. "
            "The available legal context may not be sufficient to provide a reliable answer. "
            "Please consider rephrasing your question or consulting a legal professional."
        )

    # Build context from retrieved sections
    context_parts = []
    for i, ref in enumerate(references, 1):
        part = f"Reference {i}:\n"
        part += f"  Act: {ref.get('act', 'Unknown')}\n"
        part += f"  Section: {ref.get('section', 'Unknown')}\n"
        if ref.get("title"):
            part += f"  Title: {ref['title']}\n"
        if ref.get("legal_text"):
            part += f"  Legal Provision: {ref['legal_text']}\n"
        part += f"  Related Fact Pattern: {ref['text']}\n"
        part += f"  Relevance Score: {ref['score']}\n"
        context_parts.append(part)

    context = "\n".join(context_parts)

    prompt = f"""A user has asked the following legal question:

"{query}"

Based on our legal database search using a fine-tuned LegalBERT model, the following relevant legal provisions were retrieved:

{context}

Please provide a clear, helpful legal explanation following these rules:

1. Answer the user's question using ONLY the retrieved legal context above.
2. Explain the relevant legal concepts in simple, understandable language.
3. Mention the specific sections and acts when referring to legal provisions.
4. Clearly distinguish between what is stated in the retrieved legal provisions and your general explanation.
5. Do NOT invent or fabricate any laws, sections, or legal provisions not present in the context.
6. If the retrieved legal context does not fully address the question, clearly state that the available information may be insufficient.
7. End with a note that this is general legal information for educational purposes, not legal advice.

Provide a well-structured response with clear paragraphs."""

    try:
        completion = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a legal information assistant for Indian law. You provide "
                        "clear, accurate explanations of legal provisions based on retrieved "
                        "legal context. You never fabricate laws or sections. You always "
                        "distinguish between retrieved legal provisions and general explanation."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("[RAG LLM ERROR]:", repr(e))
        return (
            "The AI explanation service encountered an error. "
            f"Error: {type(e).__name__}: {e}"
        )


# Preserved: original single-section explanation for /predict endpoint
def generate_section_explanation(section_code: str, example_text: str) -> str:
    """
    Use OpenAI Chat Completions API to generate a short, clear explanation
    of the given IPC section, linked to the example fact pattern.
    """
    if openai_client is None:
        return (
            "Explanation service is not configured. "
            "Please set the GEMINI_API_KEY environment variable."
        )

    sec_info = get_section_info(section_code)
    section_label = section_code
    legal_text_context = ""
    if sec_info:
        section_label = f"{sec_info['act']} Section {sec_info['section']}"
        if sec_info.get("title"):
            section_label += f" ({sec_info['title']})"
        if sec_info.get("legal_text"):
            legal_text_context = f"\nActual legal provision: \"{sec_info['legal_text']}\"\n"

    prompt = f"""Explain {section_label} clearly and simply.
{legal_text_context}
Example fact pattern: "{example_text}"

Requirements:
- 5 to 7 sentences.
- Describe what this section generally covers.
- Explain how it applies to the example.
- Add a final sentence that this is general information, not legal advice.
- Write as one continuous paragraph, no bullet points, no headings.
"""

    try:
        completion = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal assistant specialized in Indian Penal Code (IPC). "
                               "You explain sections in simple, accurate language."
                },
                {
                    "role": "user",
                    "content": prompt.strip()
                },
            ],
            max_tokens=350,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("[LLM ERROR]:", repr(e))
        return (
            "Gemini could not generate an explanation right now. "
            f"API error: {type(e).__name__}: {e}"
        )


# ---------------------------------------
# STARTUP
# ---------------------------------------

@app.on_event("startup")
def load_model_and_data():
    global MODEL, SECTIONS_DF, SECTION_EMBS, SECTION_IDS

    # Initialize database
    init_db()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model path not found: {MODEL_PATH}")

    print(f"[startup] Loading SentenceTransformer model from: {MODEL_PATH}")
    MODEL = SentenceTransformer(str(MODEL_PATH))

    if CSV_PATH.exists():
        print(f"[startup] Loading merged sections from CSV: {CSV_PATH}")
        SECTIONS_DF = pd.read_csv(CSV_PATH)
    else:
        print("[startup] CSV not found, building from Excel once...")
        SECTIONS_DF = build_sections_from_excels()
        SECTIONS_DF.to_csv(CSV_PATH, index=False)
        print(f"[startup] Saved merged CSV to: {CSV_PATH}")

    if "section" not in SECTIONS_DF.columns or "text" not in SECTIONS_DF.columns:
        raise RuntimeError("Section DataFrame must contain 'section' and 'text' columns")

    SECTION_EMBS = None
    SECTION_IDS = None

    if EMB_PATH.exists() and ID_PATH.exists():
        try:
            print("[startup] Found cache, loading embeddings from disk...")
            SECTION_EMBS = np.load(EMB_PATH)
            with open(ID_PATH, "r", encoding="utf-8") as f:
                SECTION_IDS = [line.strip() for line in f.readlines()]
            print(f"[startup] Loaded {len(SECTION_IDS)} cached embeddings.")
            if len(SECTION_IDS) != len(SECTIONS_DF):
                print("[startup] WARNING: cache size mismatch, ignoring cache.")
                SECTION_EMBS = None
                SECTION_IDS = None
        except Exception as e:
            print(f"[startup] Failed to load cache ({e}), will compute lazily.")
            SECTION_EMBS = None
            SECTION_IDS = None

    print("[startup] Startup finished (model + CSV loaded, DB initialized).")
    if SECTION_EMBS is None:
        print("[startup] Embeddings will be computed on first query.")
    else:
        print("[startup] Embeddings ready from cache.")


# =======================================
# ROUTES
# =======================================

# --- API Routes Below ---


# --- API: Legal Q&A (RAG pipeline) ---

@app.post("/legal/query")
def legal_query(inp: LegalQueryIn):
    """
    RAG pipeline endpoint:
    1. Use fine-tuned LegalBERT to retrieve Top-K sections
    2. Construct context from retrieved sections
    3. Generate explanation using Gemini Flash
    4. Return answer + references
    """
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    raw_query = inp.query.strip()
    if not raw_query:
        raise HTTPException(status_code=400, detail="Empty query")

    # Step 1 & 2: Retrieve using our fine-tuned LegalBERT
    references = retrieve_top_k(raw_query, k=TOP_K)

    # Step 3: Generate RAG explanation
    answer = generate_rag_explanation(raw_query, references)

    return {
        "answer": answer,
        "references": references,
        "disclaimer": (
            "LawBot 2.0 provides AI-generated legal information for educational "
            "and informational purposes and is not a substitute for advice from "
            "a qualified legal professional."
        ),
    }


# --- API: Legacy predict (preserved) ---

@app.post("/predict")
def predict(inp: QueryIn):
    """Legacy endpoint preserved for backward compatibility."""
    global MODEL, SECTIONS_DF, SECTION_EMBS, SECTION_IDS

    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    raw_query = (inp.query or inp.text or "").strip()
    if not raw_query:
        raise HTTPException(status_code=400, detail="Empty query")

    ensure_embeddings_ready()

    query_emb = MODEL.encode([raw_query], convert_to_numpy=True)[0]
    sims = cosine_sim(query_emb, SECTION_EMBS)

    topk_idx = np.argsort(-sims)[:3]

    if float(sims[topk_idx[0]]) < MIN_RELEVANCE_SCORE:
        return {
            "results": [],
            "best_explanation": None,
        }

    results = []
    for idx in topk_idx:
        sec = SECTION_IDS[idx]
        text = SECTIONS_DF.iloc[idx]["text"]
        score = float(sims[idx])

        results.append({
            "section": sec,
            "score": round(score, 6),
            "confidence": score_to_confidence(score),
            "text": text
        })

    # Generate explanation for top match
    best = results[0]
    explanation = generate_section_explanation(
        best["section"],
        best["text"]
    )
    best["explanation"] = explanation

    return {
        "results": results,
        "best_explanation": explanation
    }


# --- API: Document Analysis ---

@app.post("/documents/analyze")
async def analyze_doc(file: UploadFile = File(...)):
    """Upload and analyze a legal document (PDF)."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    # Extract text
    try:
        text, page_count = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error extracting text from PDF: {e}"
        )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from this PDF. It may be a scanned document."
        )

    # Analyze
    analysis = analyze_document(text, file.filename)

    return {
        "filename": file.filename,
        "page_count": page_count,
        "summary": analysis["summary"],
        "clauses": analysis["clauses"],
        "metadata": analysis["metadata"],
    }


# --- API: Lawyer Connect ---

@app.get("/lawyers")
def get_lawyers(
    specialization: str = Query(default=None),
    location: str = Query(default=None),
    language: str = Query(default=None),
):
    """Get lawyers with optional filters."""
    lawyers = db_get_lawyers(specialization, location, language)
    return {"lawyers": lawyers}


@app.get("/lawyers/filters")
def get_lawyer_filters():
    """Get available filter options for dropdowns."""
    return get_filter_options()


@app.get("/lawyers/{lawyer_id}")
def get_lawyer(lawyer_id: int):
    """Get a single lawyer by ID."""
    lawyer = get_lawyer_by_id(lawyer_id)
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found.")
    return lawyer


@app.post("/consultations")
def submit_consultation(data: ConsultationIn):
    """Submit a consultation request."""
    result = create_consultation_request(data.model_dump())
    return result


@app.get("/consultations")
def list_consultations():
    """List all consultation requests (demo)."""
    return {"requests": get_consultation_requests()}


# --- API: Evaluation ---

@app.get("/evaluation/data")
def evaluation_data():
    """Get evaluation metrics and model information."""
    return get_evaluation_data()


# --- Static Frontend Serving ---

# Mount the entire frontend directory at the root to serve HTML, CSS, and JS
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
    print(f"[startup] Static frontend mounted from: {FRONTEND_DIR}")

# ---------------------------------------
# ENTRY POINT
# ---------------------------------------

if __name__ == "__main__":
    import uvicorn

    print("\n=== STARTING LawBot 2.0 SERVER ===")
    print("Open this in your browser:  http://127.0.0.1:8000\n")

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
