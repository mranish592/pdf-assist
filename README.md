## PDF Assist

A RAG-based application for legal document search and Q&A, built with FastAPI, LangChain, and Streamlit.

### Features
- Upload and process PDF documents
- Search through documents with page and line references
- Ask questions about document contents using RAG (Retrieval Augmented Generation)
- Simple and intuitive web interface

### Prerequisites
- Python 3.8+
- Groq API key (sign up at https://console.groq.com)

### Installation

#### 1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-assist
```

#### 2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual Groq API key
# Replace 'your-groq-api-key-here' with your actual API key
```

Note: The `.env` file is ignored by git to keep your API key secure. Never commit your actual API keys to version control.

### Running the Application

1. Start the FastAPI backend:
```bash
# Open a new terminal and activate the virtual environment
cd backend
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
uvicorn main:app --reload
```
The backend will be available at http://localhost:8000

2. In a new terminal, start the Streamlit frontend:
```bash
# Open a new terminal and activate the virtual environment
cd frontend
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
streamlit run app.py
```
The frontend will open automatically in your default browser (typically at http://localhost:8501)

### Usage

1. Upload a PDF document using the file uploader
2. Use the search bar to find specific text within the document
3. Ask questions about the document content using the Q&A interface
4. Results will include page and line references for easy citation

### API Endpoints

- `POST /upload`: Upload and process a PDF file
- `POST /search`: Search for relevant text passages
- `POST /ask`: Ask questions about the document content

### Development

- Backend code is in the `backend/` directory
- Frontend code is in the `frontend/` directory
- Uses Annoy for vector storage and similarity search
- Implements RAG using LangChain and Groq

### Notes

- All data is stored in memory and cleared when the application restarts
- For production use, consider implementing persistent storage
- The application uses the Mixtral-8x7b model via Groq for generating answers
- Uses Spotify's Annoy library for efficient similarity search
- Simple architecture focused on stability and ease of use
