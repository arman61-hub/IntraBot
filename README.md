# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1

A secure **Company Internal Chatbot** built using **Retrieval-Augmented Generation (RAG)** and **strict Role-Based Access Control (RBAC)**.  
The system ensures that users can **only retrieve information authorized for their role**, eliminating cross-department data leakage while still allowing access to company-wide documents.

---

## 🚀 Project Overview

This project implements a **role-aware RAG pipeline** for internal company documents, strictly following the project specification provided in the PDF.

### Key Guarantees
- 🔒 Users can access **only role-permitted documents**
- 🛡️ No cross-department or privilege-escalation leakage
- 📊 Secure, auditable, and scalable retrieval
- 🧠 Vector-based semantic search with enforced RBAC filtering
- 📄 Company-wide (general) documents accessible to all employees

---

## 👥 Supported Roles

- **Finance**
- **Marketing**
- **HR**
- **Engineering**
- **Employees** (general access only)
- **C-Level** (access to all departments)

## 🔐 Access Rules

| Role        | Accessible Folders                                  |
|--------------|-----------------------------------------------------|
| Finance      | `finance + general`                               |
| Marketing    | `marketing + general`                             |
| HR           | `hr + general`                                    |
| Engineering  | `engineering + general`                           |
| Employees    | `general`                                          |
| C-Level      | `finance + marketing + hr + engineering + general` |

---

## 📂 Data Organization

Documents are organized department-wise:

```bash
data/
└── Fintech-data/
    ├── finance/
    ├── marketing/
    ├── hr/
    ├── engineering/
    └── general/

```
---

## 📄 Supported File Formats

The system supports multiple document formats commonly used in internal company knowledge bases:

- **Markdown (`.md`)** – Policy documents, reports, technical notes
- **CSV (`.csv`)** – Structured data such as financial tables or analytics
- **Text (`.txt`)** – Plain text documentation and logs

All supported formats are parsed and normalized before being ingested into the vector database.

---

## 🏗️ Architecture Summary

### Core Components

#### 🔐 RBAC Layer
- Maps **roles → allowed document folders**
- Centralized access-control logic
- Prevents unauthorized folder ingestion and retrieval

#### 🧹 Document Preprocessing Pipeline
- File parsing (Markdown, CSV, Text)
- Text cleaning and normalization
- Token-safe, model-aware chunking
- Role-based metadata injection per chunk

#### 🧠 Vector Store
- SentenceTransformer-based embeddings (```all-MiniLM-L6-v2```)
- Persistent **ChromaDB** storage
- Metadata preserved for every embedded chunk

#### 🔎 Secure Retriever
- Similarity-based vector search
- **Post-retrieval RBAC enforcement**
- Unauthorized queries safely return zero results

#### 📊 Progress Demo
- Terminal-based end-to-end execution
- Mentor-review ready demonstration
- Clearly showcases RBAC security guarantees

---

## 🔄 Processing Pipeline

```text
User Role
↓
RBAC Folder Validation
↓
Document Parsing
↓
Text Cleaning & Normalization
↓
Token-Safe Chunking
↓
Role-Based Metadata Injection
↓
Embedding Generation
↓
ChromaDB Storage
↓
Secure RBAC-Aware Retrieval

```


---

## 🔐 Security Model (RBAC)

Role-Based Access Control (RBAC) is enforced at the **retrieval layer**, ensuring that access control is applied even after semantic similarity search.

### Key Security Principles
- RBAC is enforced **after vector retrieval**
- Role metadata is stored **server-side only**
- User queries never infer or expose permissions
- Unauthorized access safely returns **zero results**

### This Prevents
- Privilege escalation
- Vector-based data leakage
- Metadata tampering
- Cross-role inference attacks

---

## 📌 Milestone 1 :  Environment Setup & Document Preprocessing
### ✅ Implemented
- Project environment setup
- Role → department access mapping
- Document parsing (`.md`, `.csv`, `.txt`)
- Text cleaning and normalization
- Token-safe chunking

## 📌 Milestone 2 :  Vector Database & Secure Retrieval
### ✅ Implemented
- SentenceTransformer embeddings (MiniLM)
- Persistent ChromaDB vector store
- High-recall semantic retrieval
- RBAC-safe post-retrieval filtering
- Duplicate chunk suppression
- End-to-end progress demo

---

## 📊 Current Results (Verified from Demo Runs)

### ✅ Authorized Query Example

```text
User Role : Finance
Query     : financial report revenue

```

- **Total documents loaded**: 21  
- **Total chunks created**: 21  
- **Results returned**: 5  
- **RBAC validation**: **PASS**

✔️ Only finance-authorized content was returned.

### 🚫 Unauthorized Query Example

```text
User Role : Marketing
Query     : employee salary

```

- **Total documents loaded**: 35 
- **Total chunks created**: 35
- **Results returned**: 0
- **RBAC validation**: **PASS**

✔️ Unauthorized access was correctly blocked with zero results.
---

## 🧪 How to Run Progress Demo

From the project root:

```bash
python -m backend.tests.progress.progress_demo
```

## 📁 Project Structure (Current)
```bash
Chatbot/
├── backend/
│   ├── app/
│   │   ├── rag/
│   │   │   ├── rbac.py              # Role → document access rules
│   │   │   ├── preprocessing.py     # Parse, clean, chunk, metadata
│   │   │   ├── vector_store.py      # Embeddings + ChromaDB
│   │   │   ├── retriever.py         # Secure RBAC-aware retrieval
│   │   │   ├── pipeline.py          # End-to-end orchestration
│   │   │   └── __init__.py
│   │   │
│   │   ├── vector_db/
│   │   │   └── chroma/              # Persistent vector storage
│   │   │
│   │   └── main.py                  # (Future FastAPI entry point)
│   │
│   ├── tests/
│   │   └── progress/
│   │       └── progress_demo.py     # Mentor demo script
│   │
│   └── requirements.txt
│
├── data/
│   └── Fintech-data/
│       ├── finance/
│       ├── marketing/
│       ├── hr/
│       ├── engineering/
│       └── general/
│
├── frontend/
│   └── streamlit_app.py             # (Future UI)
│
└── README.md
```