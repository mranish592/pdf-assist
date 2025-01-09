import streamlit as st
import requests
import json
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('frontend.log')
    ]
)
logger = logging.getLogger(__name__)

# Constants
API_URL = "http://localhost:8000"
logger.info("Starting Streamlit application")

st.title("Legal Documents Q&A System")

# File upload
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
if uploaded_file:
    logger.info(f"File uploaded: {uploaded_file.name}")
    try:
        files = {"file": uploaded_file}
        logger.debug("Sending file to backend")
        response = requests.post(f"{API_URL}/upload", files=files)
        
        if response.status_code == 200:
            logger.info("File processed successfully")
            st.success("File uploaded and processed successfully!")
        else:
            logger.error(f"Backend error: {response.status_code} - {response.text}")
            st.error(f"Error processing file: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error: {str(e)}", exc_info=True)
        st.error("Could not connect to backend server")

# Search functionality
st.subheader("Search Documents")
search_query = st.text_input("Enter search terms")
if search_query:
    logger.info(f"Search query: {search_query}")
    try:
        response = requests.post(
            f"{API_URL}/search",
            json={"text": search_query},
            timeout=30
        )
        
        if response.status_code == 200:
            results = response.json()
            logger.info(f"Received {len(results)} search results")
            for doc in results:
                st.write(f"Page {doc['metadata']['page']}, Line {doc['metadata']['line']}:")
                st.write(doc['content'])
                st.markdown("---")
        else:
            logger.error(f"Search error: {response.status_code} - {response.text}")
            st.error("Error performing search")
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error during search: {str(e)}", exc_info=True)
        st.error("Could not connect to backend server")

# Question answering
st.subheader("Ask Questions")
question = st.text_input("Enter your question")
if question:
    logger.info(f"Question asked: {question}")
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"text": question},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info("Received answer from backend")
            
            st.write("Answer:")
            st.write(result["answer"])
            
            st.write("Sources:")
            for source in result["sources"]:
                st.write(f"Page {source['metadata']['page']}, Line {source['metadata']['line']}:")
                st.write(source['content'])
                st.markdown("---")
        else:
            logger.error(f"Question answering error: {response.status_code} - {response.text}")
            st.error("Error getting answer")
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error during question: {str(e)}", exc_info=True)
        st.error("Could not connect to backend server") 