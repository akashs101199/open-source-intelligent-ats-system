"""
Service for document processing and text extraction
"""
import PyPDF2
import docx
import logging
from io import BytesIO
from typing import Optional

logger = logging.getLogger(__name__)

class DocumentService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            return file_content.decode('utf-8', errors='ignore').strip()
        except Exception as e:
            logger.error(f"TXT extraction error: {e}")
            return ""
    
    @staticmethod
    def extract_text(file_content: bytes, filename: str) -> str:
        """Extract text based on file extension"""
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.pdf'):
            return DocumentService.extract_text_from_pdf(file_content)
        elif filename_lower.endswith('.docx'):
            return DocumentService.extract_text_from_docx(file_content)
        elif filename_lower.endswith('.txt'):
            return DocumentService.extract_text_from_txt(file_content)
        else:
            # Try as plain text
            return DocumentService.extract_text_from_txt(file_content)

document_service = DocumentService()