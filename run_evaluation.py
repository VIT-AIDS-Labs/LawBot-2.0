import pandas as pd
import numpy as np
import time
import os
import glob
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from backend.legal_sections import IPC_SECTIONS

def main():
    # 1. Load data
    df_all = pd.read_csv('data/sections_clean.csv')
    df_all.columns = ['section', 'text']
    df_all = df_all[df_all['section'] != 'section_id'].dropna().copy()
    
    # 2. Find test data
    train_files = glob.glob('data/train_*.xlsx')
    train_queries = set()
    for f in train_files:
        df_train = pd.read_excel(f)
        if 'query_text' in df_train.columns:
            train_queries.update(df_train['query_text'].dropna().tolist())
        elif 'text' in df_train.columns:
            train_queries.update(df_train['text'].dropna().tolist())
            
    df_test = df_all[~df_all['text'].isin(train_queries)].copy()
    if df_test.empty or len(df_test) < 50:
        print("No or too few test data found by exclusion. Splitting last 20% as test.")
        df_test = df_all.iloc[int(len(df_all)*0.8):].copy()

    print(f"Total dataset: {len(df_all)}, Test set: {len(df_test)}")
    
    # 3. Load Model
    start_time = time.time()
    # load local model
    model = SentenceTransformer('.')
    load_time = time.time() - start_time
    print(f"Model loaded in {load_time:.2f}s")
    
    # 4. Prepare Corpus
    section_ids = list(IPC_SECTIONS.keys())
    section_texts = [IPC_SECTIONS[sid]['legal_text'] for sid in section_ids]
    
    print("Encoding corpus...")
    corpus_embeddings = model.encode(section_texts, convert_to_tensor=True)
    
    # 5. Evaluate
    print("Evaluating test set...")
    queries = df_test['text'].tolist()
    true_labels = df_test['section'].tolist()
    
    start_time = time.time()
    query_embeddings = model.encode(queries, convert_to_tensor=True, batch_size=32)
    inference_time = (time.time() - start_time) / len(queries)
    
    from sentence_transformers.util import semantic_search
    hits = semantic_search(query_embeddings, corpus_embeddings, top_k=5)
    
    top1_correct = 0
    top3_correct = 0
    top5_correct = 0
    
    y_pred = []
    
    for idx, hit_list in enumerate(hits):
        true_label = true_labels[idx]
        retrieved_sections = [section_ids[hit['corpus_id']] for hit in hit_list]
        
        y_pred.append(retrieved_sections[0])
        
        if true_label in retrieved_sections[:1]:
            top1_correct += 1
        if true_label in retrieved_sections[:3]:
            top3_correct += 1
        if true_label in retrieved_sections[:5]:
            top5_correct += 1
            
    n = len(queries)
    top1 = top1_correct/n
    top3 = top3_correct/n
    top5 = top5_correct/n
    
    print(f"Top-1 Accuracy: {top1:.4f}")
    print(f"Top-3 Accuracy: {top3:.4f}")
    print(f"Top-5 Accuracy: {top5:.4f}")
    print(f"Avg inference time: {inference_time*1000:.2f} ms")
    
    # Classification metrics (Top-1)
    # filter out true_labels that might not be in IPC_SECTIONS?
    # Actually all should be there, but just in case.
    valid_indices = [i for i, t in enumerate(true_labels) if t in section_ids]
    y_true_valid = [true_labels[i] for i in valid_indices]
    y_pred_valid = [y_pred[i] for i in valid_indices]
    
    acc = accuracy_score(y_true_valid, y_pred_valid)
    prec = precision_score(y_true_valid, y_pred_valid, average='weighted', zero_division=0)
    rec = recall_score(y_true_valid, y_pred_valid, average='weighted', zero_division=0)
    f1 = f1_score(y_true_valid, y_pred_valid, average='weighted', zero_division=0)
    
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-score: {f1:.4f}")
    
    # save plot
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Top-3 Acc', 'Top-5 Acc']
    values = [acc, prec, rec, f1, top3, top5]
    
    plt.figure(figsize=(10,6))
    sns.barplot(x=metrics, y=values)
    plt.title('Performance Metrics')
    plt.ylim(0, 1)
    for i, v in enumerate(values):
        plt.text(i, v + 0.02, f"{v:.4f}", ha='center')
    plt.tight_layout()
    plt.savefig('performance_chart.png')
    
    # confusion matrix
    cm_labels = sorted(list(set(y_true_valid)))
    if len(cm_labels) > 20:
        cm_labels = cm_labels[:20] # truncate for visibility if needed, but let's just plot all
    cm = confusion_matrix(y_true_valid, y_pred_valid, labels=cm_labels)
    plt.figure(figsize=(14,12))
    sns.heatmap(cm, xticklabels=cm_labels, yticklabels=cm_labels, cmap='Blues', annot=False)
    plt.title('Confusion Matrix (Top-1) - Top 20 Classes for Visibility')
    plt.ylabel('True Section')
    plt.xlabel('Predicted Section')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    
    # Write report
    with open('evaluation_report.txt', 'w') as f:
        f.write("Model Evaluation Report\n")
        f.write("========================\n\n")
        f.write(f"Total dataset size: {len(df_all)}\n")
        f.write(f"Test dataset size (held-out): {len(df_test)}\n\n")
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision (weighted): {prec:.4f}\n")
        f.write(f"Recall (weighted): {rec:.4f}\n")
        f.write(f"F1-score (weighted): {f1:.4f}\n\n")
        f.write(f"Top-1 Accuracy: {top1:.4f}\n")
        f.write(f"Top-3 Accuracy: {top3:.4f}\n")
        f.write(f"Top-5 Accuracy: {top5:.4f}\n\n")
        f.write(f"Avg Inference Time per Query: {inference_time*1000:.2f} ms\n")

if __name__ == "__main__":
    main()
