# backend/evaluation.py
"""
Evaluation metrics module for LawBot 2.0.
Provides model information and training metrics extracted from the project.
"""

from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent


def get_evaluation_data() -> dict:
    """
    Return evaluation data including model info, training metrics,
    and placeholder evaluation metrics.
    """
    return {
        "model_info": {
            "base_model": "nlpaueb/legal-bert-base-uncased",
            "model_type": "SentenceTransformer",
            "embedding_dimension": 768,
            "max_sequence_length": 512,
            "similarity_function": "Cosine Similarity",
            "pooling_mode": "Mean Tokens",
            "architecture": "BertModel + Pooling",
        },
        "training_details": {
            "dataset_size": 23481,
            "training_epochs": 6,
            "batch_size": 8,
            "loss_function": "MultipleNegativesRankingLoss",
            "optimizer": "AdamW (fused)",
            "learning_rate": 5e-05,
            "seed": 42,
            "framework_versions": {
                "python": "3.12.12",
                "sentence_transformers": "5.1.2",
                "transformers": "4.57.1",
                "pytorch": "2.8.0+cu126",
            },
        },
        "training_metrics": [
            {"epoch": 0.17, "step": 500, "loss": 0.3705},
            {"epoch": 0.34, "step": 1000, "loss": 0.1711},
            {"epoch": 0.51, "step": 1500, "loss": 0.1441},
            {"epoch": 0.68, "step": 2000, "loss": 0.1351},
            {"epoch": 0.85, "step": 2500, "loss": 0.1306},
            {"epoch": 1.02, "step": 3000, "loss": 0.1208},
            {"epoch": 1.19, "step": 3500, "loss": 0.1275},
            {"epoch": 1.36, "step": 4000, "loss": 0.1180},
            {"epoch": 1.53, "step": 4500, "loss": 0.1245},
            {"epoch": 1.70, "step": 5000, "loss": 0.1281},
            {"epoch": 1.87, "step": 5500, "loss": 0.1376},
            {"epoch": 2.04, "step": 6000, "loss": 0.1109},
            {"epoch": 2.21, "step": 6500, "loss": 0.1236},
            {"epoch": 2.38, "step": 7000, "loss": 0.1212},
            {"epoch": 2.55, "step": 7500, "loss": 0.1255},
            {"epoch": 2.72, "step": 8000, "loss": 0.1196},
            {"epoch": 2.90, "step": 8500, "loss": 0.1179},
            {"epoch": 3.07, "step": 9000, "loss": 0.1179},
            {"epoch": 3.24, "step": 9500, "loss": 0.1251},
            {"epoch": 3.41, "step": 10000, "loss": 0.1188},
            {"epoch": 3.58, "step": 10500, "loss": 0.1151},
            {"epoch": 3.75, "step": 11000, "loss": 0.1186},
            {"epoch": 3.92, "step": 11500, "loss": 0.1103},
            {"epoch": 4.09, "step": 12000, "loss": 0.1182},
            {"epoch": 4.26, "step": 12500, "loss": 0.1156},
            {"epoch": 4.43, "step": 13000, "loss": 0.1150},
            {"epoch": 4.60, "step": 13500, "loss": 0.1258},
            {"epoch": 4.77, "step": 14000, "loss": 0.1164},
            {"epoch": 4.94, "step": 14500, "loss": 0.1182},
            {"epoch": 5.11, "step": 15000, "loss": 0.1162},
            {"epoch": 5.28, "step": 15500, "loss": 0.1133},
            {"epoch": 5.45, "step": 16000, "loss": 0.1183},
            {"epoch": 5.62, "step": 16500, "loss": 0.1133},
            {"epoch": 5.79, "step": 17000, "loss": 0.1142},
            {"epoch": 5.96, "step": 17500, "loss": 0.1161},
        ],
        "system_config": {
            "llm": "Gemini Flash",
            "retrieval_method": "Top-K Cosine Similarity",
            "min_relevance_score": 0.65,
            "top_k": 3,
            "rag_pipeline": "LegalBERT + Gemini",
        },
        "evaluation_metrics": {
            "retrieval": {
                "accuracy": None,
                "precision": None,
                "recall": None,
                "f1_score": None,
                "top_k_accuracy": None,
                "status": "Evaluation in progress",
            },
            "document_analysis": {
                "rouge_score": None,
                "clause_precision": None,
                "clause_recall": None,
                "status": "Evaluation in progress",
            },
        },
    }
