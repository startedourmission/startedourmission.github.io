#!/usr/bin/env python3
"""Generate RAG pipeline diagram for CME295 Chapter 7."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, conn, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout (left to right)
y_main = 200
x_query = 80
x_retriever = 280
x_kb = 280
x_augmented = 480
x_llm = 640
x_response = 800
y_kb = 80  # Knowledge base above retriever

# --- Query ---
elements.append(box(nid(), x_query, y_main, 100, 44))
elements.append(text(nid(), x_query, y_main, "Query", size=16))

# Arrow to retriever
elements.append(arrow(nid(), x_query + 50, y_main, x_retriever - 80, y_main))

# --- Retriever ---
elements.append(box(nid(), x_retriever, y_main, 140, 50))
elements.append(text(nid(), x_retriever, y_main - 8, "Retriever", size=16))
elements.append(text(nid(), x_retriever, y_main + 12, "Embedding + Similarity", size=11))

# --- Knowledge Base (stacked documents effect) ---
# Three stacked rectangles to look like documents
for offset in [8, 4, 0]:
    elements.append(box(nid(), x_kb + offset, y_kb - offset, 130, 50, thin=(offset != 0)))
elements.append(text(nid(), x_kb, y_kb, "Knowledge Base", size=13))

# Arrow between KB and retriever (bidirectional conceptually, use conn + arrows)
elements.append(arrow(nid(), x_kb, y_kb + 25, x_retriever, y_main - 25))

# --- Retrieved chunks arrow to Augmented Prompt ---
elements.append(arrow(nid(), x_retriever + 70, y_main, x_augmented - 75, y_main))
elements.append(text(nid(), (x_retriever + x_augmented) / 2, y_main - 22, "Retrieved chunks", size=11))

# --- Augmented Prompt ---
elements.append(box(nid(), x_augmented, y_main, 130, 50))
elements.append(text(nid(), x_augmented, y_main - 8, "Augmented", size=14))
elements.append(text(nid(), x_augmented, y_main + 12, "Prompt", size=14))

# Arrow to LLM
elements.append(arrow(nid(), x_augmented + 65, y_main, x_llm - 55, y_main))

# --- LLM ---
elements.append(box(nid(), x_llm, y_main, 90, 50))
elements.append(text(nid(), x_llm, y_main, "LLM", size=18))

# Arrow to Response
elements.append(arrow(nid(), x_llm + 45, y_main, x_response - 55, y_main))

# --- Response ---
elements.append(box(nid(), x_response, y_main, 100, 44))
elements.append(text(nid(), x_response, y_main, "Response", size=16))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-rag-pipeline.excalidraw"
save(out_path, elements)
print("Done: RAG pipeline diagram")
