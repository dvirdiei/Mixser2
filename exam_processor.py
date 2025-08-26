#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backend wrapper for integrating the advanced PDF exam shuffling system
with our Flask frontend
"""

import os
import tempfile
import shutil
import subprocess
from pathlib import Path

# Check if Tesseract is available
def check_tesseract():
    """Check if Tesseract OCR is available"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

# Set Tesseract path for different environments
def setup_tesseract():
    """Setup Tesseract path for different environments"""
    if not check_tesseract():
        # Try common paths
        possible_paths = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract',
            'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
            'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                os.environ['PATH'] = os.path.dirname(path) + os.pathsep + os.environ.get('PATH', '')
                break
    
    # Set TESSDATA_PREFIX if not set
    if 'TESSDATA_PREFIX' not in os.environ:
        tessdata_paths = [
            '/usr/share/tesseract-ocr/4.00/tessdata/',
            '/usr/share/tesseract-ocr/tessdata/',
            '/usr/local/share/tessdata/',
            'C:\\Program Files\\Tesseract-OCR\\tessdata\\'
        ]
        
        for path in tessdata_paths:
            if os.path.exists(path):
                os.environ['TESSDATA_PREFIX'] = path
                break

# Initialize Tesseract
setup_tesseract()

# Import the backend system
try:
    import sys
    import os
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    from Main import main as backend_main
    from Main import get_ouput_directory
except ImportError as e:
    print(f"Failed to import backend: {e}")
    raise

class ExamShuffler:
    """
    Wrapper class for the advanced PDF exam shuffling backend
    """
    
    def __init__(self, temp_dir=None):
        """
        Initialize the exam shuffler
        
        Args:
            temp_dir: Directory for temporary files (optional)
        """
        self.temp_dir = temp_dir or tempfile.mkdtemp()
        self.output_directory = get_ouput_directory()
        
        # Create necessary directories
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_directory, exist_ok=True)
        os.makedirs("Final PDFs", exist_ok=True)
    
    def shuffle_pdf_exam(self, input_pdf_path, output_pdf_path=None):
        """
        Process a single PDF exam and shuffle it
        
        Args:
            input_pdf_path: Path to the input PDF file
            output_pdf_path: Path for the output PDF (optional)
            
        Returns:
            tuple: (success_status, output_path, error_message)
        """
        try:
            # Ensure input file exists
            if not os.path.exists(input_pdf_path):
                return False, None, f"Input file does not exist: {input_pdf_path}"
            
            # Process the PDF using the backend
            success_pdfs, success_flag = backend_main([input_pdf_path])
            
            if not success_flag or not success_pdfs:
                return False, None, "Backend processing failed"
            
            # Get the generated PDF path
            generated_pdf = success_pdfs[0]
            
            # If output path is specified, copy the file there
            if output_pdf_path:
                shutil.copy2(generated_pdf, output_pdf_path)
                final_path = output_pdf_path
            else:
                final_path = generated_pdf
                
            return True, final_path, None
            
        except Exception as e:
            return False, None, str(e)
    
    def cleanup(self):
        """
        Clean up temporary files and directories
        """
        try:
            # Clean up the backend's temporary files
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                
            # Clean up backend output directory
            output_dir = self.output_directory
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    file_path = os.path.join(output_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception:
                        pass
                        
        except Exception:
            pass

def process_exam_pdf(input_path, output_path=None):
    """
    Convenience function for processing a single PDF exam
    
    Args:
        input_path: Path to input PDF
        output_path: Path for output PDF (optional)
        
    Returns:
        tuple: (success_status, output_path, error_message)
    """
    # Check if Tesseract is available before processing
    if not check_tesseract():
        error_msg = "Tesseract OCR is not installed or not accessible. Please install tesseract-ocr package."
        print(f"ERROR: {error_msg}")
        return False, None, error_msg
    
    shuffler = ExamShuffler()
    try:
        result = shuffler.shuffle_pdf_exam(input_path, output_path)
        return result
    finally:
        shuffler.cleanup()

# Example usage for testing
if __name__ == "__main__":
    test_pdf = r"C:\Users\HP\Downloads\ddd.pdf"
    output_pdf = r"test_shuffled_exam.pdf"
    
    success, path, error = process_exam_pdf(test_pdf, output_pdf)
    
    if success:
        print(f"Successfully created shuffled exam: {path}")
    else:
        print(f"Failed to create shuffled exam: {error}")
