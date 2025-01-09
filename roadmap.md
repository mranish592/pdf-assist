### **Concise MVP Roadmap**

#### **1\. Setup Environment**

-   Install required libraries: `langchain`, `groq`, `faiss-cpu`, `sentence-transformers`, `fastapi`, `streamlit`, `pdfplumber`.
-   Choose embedding model: Use `sentence-transformers/msmarco-distilbert-base-v3` for embeddings.

#### **2\. Backend Development**

1.  **PDF Processing:**

    -   Extract text with `pdfplumber` while preserving line and page numbers.
    -   Split text into chunks (e.g., paragraphs or sentences).
2.  **Embedding and Vector Store:**

    -   Generate embeddings using SentenceTransformers.
    -   Store embeddings in FAISS for vector search.
3.  **LangChain RAG Pipeline:**

    -   Use LangChain's `VectorStoreRetriever` to retrieve relevant chunks from the vector store.
    -   Pass the query and retrieved chunks to Groq using LangChain's LLM wrapper for answers.
4.  **API with FastAPI:**

    -   Endpoints:
        -   `/upload`: Process and store PDF text.
        -   `/search`: Return matching text with line/page metadata.
        -   `/ask`: Answer questions using RAG pipeline.

#### **3\. Frontend Development**

1.  **Streamlit UI:**

    -   Upload PDFs.
    -   Search bar for keyword search.
    -   Input box for asking questions.
    -   Display search results with line/page numbers and Q&A responses.
2.  **Backend Integration:**

    -   Use `requests` in Streamlit to call FastAPI endpoints.

#### **4\. Privacy Implementation**

-   Process files in-memory and clear after the session.
-   Use HTTPS for secure communication.

* * * * *

With this concise roadmap, you can proceed to generate the necessary code blocks and iterate as needed.