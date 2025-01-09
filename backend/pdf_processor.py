import pdfplumber
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def process_pdf(self, file, filename: str = "uploaded_file.pdf") -> List[Dict[str, any]]:
        """Process PDF and return chunks with metadata."""
        logger.info(f"Starting to process PDF: {filename}")
        documents = []
        
        try:
            with pdfplumber.open(file) as pdf:
                logger.info(f"PDF opened successfully, total pages: {len(pdf.pages)}")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    logger.debug(f"Processing page {page_num}")
                    text = page.extract_text()
                    if not text:
                        logger.warning(f"No text found on page {page_num}")
                        continue
                    
                    lines = text.split('\n')
                    processed_lines = 0
                    for line_num, line in enumerate(lines, 1):
                        if line.strip():  # Skip empty lines
                            documents.append({
                                'content': line,
                                'metadata': {
                                    'page': page_num,
                                    'line': line_num,
                                    'source': filename
                                }
                            })
                            processed_lines += 1
                    
                    logger.debug(f"Processed {processed_lines} lines from page {page_num}")
                
                logger.info(f"PDF processing complete. Total chunks: {len(documents)}")
                return documents
                
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
            raise 