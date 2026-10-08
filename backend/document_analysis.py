# backend/document_analysis.py
"""
Legal document analysis module for LawBot 2.0.
Handles PDF upload, text extraction, summarization, and clause identification.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)


def _get_llm_client():
    """Get the LLM client (Gemini via OpenAI SDK)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, None
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    model = os.getenv("LLM_MODEL", "gemini-3.6-flash")
    return client, model


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, int]:
    """
    Extract text from PDF bytes using PyMuPDF.
    Returns (extracted_text, page_count).
    """
    import fitz  # PyMuPDF

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page_count = len(doc)
    text_parts = []

    for page_num in range(page_count):
        page = doc[page_num]
        text = page.get_text("text")
        if text.strip():
            text_parts.append(f"--- Page {page_num + 1} ---\n{text}")

    doc.close()
    full_text = "\n\n".join(text_parts)
    return full_text, page_count


def analyze_document(text: str, filename: str) -> dict:
    """
    Analyze extracted document text using Gemini.
    Returns summary, important clauses, and metadata.
    """
    client, model = _get_llm_client()

    if client is None:
        return {
            "summary": "Document analysis service is not configured. Please set the GEMINI_API_KEY.",
            "clauses": [],
            "metadata": {},
        }

    # Truncate very long documents to fit within context
    max_chars = 30000
    truncated = len(text) > max_chars
    analysis_text = text[:max_chars] if truncated else text

    prompt = f"""Analyze the following legal document and provide a structured analysis.

Document filename: {filename}
{"[Note: Document was truncated for analysis due to length]" if truncated else ""}

Document text:
\"\"\"
{analysis_text}
\"\"\"

Provide your analysis in the following exact format. Use these exact headers:

DOCUMENT_TYPE: [Identify the type of legal document, e.g., Agreement, Contract, Legal Notice, Affidavit, etc.]

SUMMARY:
[Provide a comprehensive summary of the document in 3-5 paragraphs. Cover the key parties involved, the purpose of the document, main terms and conditions, and any notable provisions.]

IMPORTANT_CLAUSES:
[For each important clause, use this format:]
CLAUSE: [Clause title or identifier]
CONTENT: [Brief description of the clause content]
IMPORTANCE: [High/Medium/Low]
---

PARTIES: [List the parties involved, separated by semicolons]

KEY_DATES: [List any important dates mentioned, separated by semicolons]

JURISDICTION: [Mention the applicable jurisdiction or governing law if stated]

Requirements:
- Focus on legally significant clauses (liability, termination, indemnity, confidentiality, dispute resolution, payment terms, etc.)
- Identify at least 3 important clauses if present
- Be factual and accurate - only report what is in the document
- If the document is not a legal document, state that clearly in the summary
"""

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a legal document analyst. You analyze legal documents "
                        "and provide structured summaries, identify important clauses, "
                        "and extract key information. Be accurate and factual."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
        )
        response_text = completion.choices[0].message.content
        return _parse_analysis_response(response_text)

    except Exception as e:
        print(f"[document_analysis] LLM error: {e}")
        return {
            "summary": f"Error analyzing document: {type(e).__name__}",
            "clauses": [],
            "metadata": {},
        }


def _parse_analysis_response(response: str) -> dict:
    """Parse the structured LLM response into a dict."""
    result = {
        "summary": "",
        "clauses": [],
        "metadata": {},
    }

    # Extract document type
    if "DOCUMENT_TYPE:" in response:
        doc_type_line = response.split("DOCUMENT_TYPE:")[1].split("\n")[0].strip()
        result["metadata"]["document_type"] = doc_type_line

    # Extract summary
    if "SUMMARY:" in response:
        summary_start = response.index("SUMMARY:") + len("SUMMARY:")
        # Find where the next section starts
        summary_end = len(response)
        for marker in ["IMPORTANT_CLAUSES:", "CLAUSE:"]:
            if marker in response[summary_start:]:
                pos = response.index(marker, summary_start)
                summary_end = min(summary_end, pos)
        result["summary"] = response[summary_start:summary_end].strip()

    # Extract clauses
    if "IMPORTANT_CLAUSES:" in response or "CLAUSE:" in response:
        clause_section = response
        if "IMPORTANT_CLAUSES:" in response:
            clause_section = response.split("IMPORTANT_CLAUSES:")[1]

        # Split by CLAUSE: markers
        clause_parts = clause_section.split("CLAUSE:")
        for part in clause_parts[1:]:  # Skip first empty part
            clause = {"title": "", "content": "", "importance": "Medium"}

            lines = part.strip().split("\n")
            clause["title"] = lines[0].strip()

            for line in lines[1:]:
                if line.strip().startswith("CONTENT:"):
                    clause["content"] = line.split("CONTENT:")[1].strip()
                elif line.strip().startswith("IMPORTANCE:"):
                    imp = line.split("IMPORTANCE:")[1].strip()
                    if imp in ("High", "Medium", "Low"):
                        clause["importance"] = imp

            # If content wasn't found with the label, use remaining text
            if not clause["content"] and len(lines) > 1:
                content_lines = [
                    l
                    for l in lines[1:]
                    if not l.strip().startswith(("IMPORTANCE:", "---", "PARTIES:", "KEY_DATES:", "JURISDICTION:"))
                    and l.strip()
                ]
                clause["content"] = " ".join(l.strip() for l in content_lines)

            if clause["title"] and (clause["content"] or clause["title"]):
                result["clauses"].append(clause)

    # Extract metadata fields
    for field, key in [("PARTIES:", "parties"), ("KEY_DATES:", "key_dates"), ("JURISDICTION:", "jurisdiction")]:
        if field in response:
            value = response.split(field)[1].split("\n")[0].strip()
            if value:
                result["metadata"][key] = value

    # Fallback: if nothing was parsed, use the entire response as summary
    if not result["summary"] and not result["clauses"]:
        result["summary"] = response.strip()

    return result
