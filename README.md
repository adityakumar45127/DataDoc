# 📊 DataDoc

### AI Business Intelligence & Document Intelligence Copilot

DataDoc is an AI-powered **Business Intelligence and Document Intelligence platform** built with Streamlit. It combines structured dataset analysis, AI-generated business insights, PDF document processing, semantic search, and Retrieval-Augmented Generation (RAG) into a single interactive workspace.

## ✨ Features

- 📊 **Dataset Analytics** — Upload CSV files, inspect dataset structure, analyze numerical and categorical features, identify missing values and duplicates, generate statistical summaries, and explore data through visualizations.
- 
- 🤖 **AI Business Insights** — Automatically generate an executive summary, important trends, business risks, and actionable recommendations from uploaded datasets.
- 
- 📄 **PDF Document Intelligence** — Upload PDF documents, extract their content, split documents into meaningful chunks, generate embeddings, and store them in a vector database.
- 
- 🔎 **RAG Question Answering** — Ask questions about uploaded documents and receive context-grounded answers with relevant page-level sources.
- 
- 🧠 **LLM Fallback Architecture** — Uses Google Gemini as the primary LLM with Ollama as a local fallback for improved reliability.
- 
- ⚡ **Smart AI Caching** — Uses SHA-256 file identification and Streamlit session state to prevent unnecessary re-analysis of the same CSV during application reruns.
- 
- 📚 **Multi-Document Support** — Process and query uploaded PDF documents independently.
- 
- 🧩 **Structured AI Output** — Uses Pydantic schemas to produce consistent business insight responses.

## 📸 Screenshots

### 🖥️ DataDoc Dashboard

![DataDoc Dashboard](assets/dashboard.png)

### 📊 Dataset Analytics

![Dataset Analytics](assets/dataset-preview.png)

### 🤖 AI Business Insights

![AI Business Insights](assets/ai-insights.png)

### 🔎 RAG Document Question Answering

![RAG Question Answering](assets/rag-answer.png)

## 🏗️ Architecture

```text
                           📊 DataDoc
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
             📊 CSV Analytics      📄 PDF Intelligence
                    │                   │
                    ▼                   ▼
             Dataset Profiling    Text Extraction
                    │                   │
                    ▼                   ▼
             Data Visualization     Chunking
                    │                   │
                    ▼                   ▼
              AI Insights          Embeddings
                                        │
                                        ▼
                                   🗄️ ChromaDB
                                        │
                                        ▼
                                  🔎 Retrieval
                                        │
                                        ▼
                                📚 Relevant Context
                                        │
                         ┌──────────────┘
                         ▼
                    🤖 LLM Layer
                 Gemini / Ollama
                         │
                         ▼
                 💬 Final Response
                         │
                         ▼
                    📌 Sources
```

## 🔎 RAG Pipeline

```text
📄 PDF
  ↓
📖 Text Extraction
  ↓
✂️ Document Chunking
  ↓
🧠 Embedding Generation
  ↓
🗄️ ChromaDB Vector Store
  ↓
🔎 Semantic Retrieval
  ↓
📚 Relevant Context
  ↓
🤖 LLM
  ↓
💬 Grounded Answer
  ↓
📌 Source Pages
```

## 🤖 LLM Reliability

DataDoc implements a primary/fallback architecture:

```text
👤 User Request
      ↓
🤖 Google Gemini
      │
   ┌──┴──┐
   │     │
  ✅     ❌
Success Failure
   │     │
   ↓     ↓
Answer 🦙 Ollama
          │
          ↓
        Answer
```

This allows the application to continue using a local Ollama model when the primary Gemini provider is unavailable or produces an invalid response.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| 🐍 Programming | Python |
| 🖥️ Application | Streamlit |
| 📊 Data Processing | Pandas, NumPy |
| 📈 Visualization | Matplotlib, Seaborn |
| 🔗 LLM Framework | LangChain |
| 🤖 Primary LLM | Google Gemini |
| 🦙 Local LLM | Ollama |
| 🗄️ Vector Database | ChromaDB |
| 🧠 Embeddings | Sentence Transformers |
| 🧩 Structured Output | Pydantic |
| 🔧 Version Control | Git, GitHub |

## 📁 Project Structure

```text
DataDoc/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   ├── data_processing/
│   │   ├── dataset_profiler.py
│   │   └── dataset_summary.py
│   │
│   ├── visualization/
│   │   └── charts.py
│   │
│   ├── llm/
│   │   ├── ai_pipeline.py
│   │   ├── gemini_client.py
│   │   ├── insight_generator.py
│   │   ├── llm_router.py
│   │   ├── output_schema.py
│   │   └── prompts.py
│   │
│   └── rag/
│       ├── chunker.py
│       ├── document_loader.py
│       ├── embeddings.py
│       ├── rag_generator.py
│       ├── rag_pipeline.py
│       ├── rag_prompt.py
│       └── vector_store.py
│
└── data/
    └── chroma_db/
```

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/adityakumar45127/DataDoc.git
cd DataDoc
```

### Create a virtual environment

**Windows**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

For the local Ollama fallback, install Ollama and pull the configured model:

```bash
ollama pull llama3.2
```

> 🔒 Never commit API keys, `.env` files, or other sensitive credentials to GitHub.

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch through the Streamlit interface.

## 🔄 Core Workflows

### 📊 CSV → AI Business Intelligence

```text
📁 Upload CSV
     ↓
🔍 Dataset Profiling
     ↓
📊 Statistical Analysis
     ↓
📈 Visualization
     ↓
🤖 AI Analysis
     ↓
┌──────────────────────────┐
│ 📝 Executive Summary     │
│ 📈 Important Trends      │
│ ⚠️ Business Risks        │
│ 💡 Recommendations       │
└──────────────────────────┘
```

### 📄 PDF → RAG → Answer

```text
📁 Upload PDF
     ↓
📖 Extract Text
     ↓
✂️ Chunk Document
     ↓
🧠 Generate Embeddings
     ↓
🗄️ Store in ChromaDB
     ↓
🔎 Retrieve Relevant Context
     ↓
🤖 Generate Answer
     ↓
💬 Answer + 📌 Sources
```

## ⚡ Engineering Highlights

- 🧠 End-to-end Retrieval-Augmented Generation pipeline
- 🗄️ ChromaDB vector database integration
- 🔎 Semantic document retrieval
- 🤖 Gemini + Ollama LLM architecture
- 🔄 Automatic LLM fallback
- 🧩 Structured LLM responses with Pydantic
- 🔐 SHA-256 based dataset identification
- ⚡ Session-state based AI insight caching
- 📚 Multi-document PDF processing
- 🧱 Modular Python architecture
- 🖥️ Interactive Streamlit application
- 🔧 Git/GitHub version-controlled development

## 🧪 Testing

The project contains RAG-related tests covering embeddings, retrieval, vector storage, and RAG generation.

Run the test suite with:

```bash
pytest
```

## 🔮 Future Enhancements

- 💬 Multi-turn conversational document chat
- 🗃️ Natural-language SQL querying
- 🎛️ Advanced dataset filtering
- 📊 Automated visualization recommendations
- 🤖 Additional LLM providers
- ☁️ Cloud vector database integration
- 🔐 Authentication and user management
- 📑 Exportable business intelligence reports
- 🚀 Production deployment

## 👨‍💻 Author

**Aditya Kumar**  
B.Tech — Electronics & Communication Engineering

**Focus:** Data Science · Machine Learning · AI Engineering · Business Intelligence

🔗 **GitHub:** https://github.com/adityakumar45127  
🔗 **LinkedIn:** https://www.linkedin.com/in/aditya-kumar45127/

---

<div align="center">

### 🐍 Python • ⚡ Streamlit • 🤖 LLMs • 🔎 RAG • 🗄️ ChromaDB

⭐ If you find DataDoc useful, consider giving the repository a star.

</div>