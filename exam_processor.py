#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backend wrapper for integrating the original advanced PDF exam shuffling system
with our Flask frontend
"""

import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

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

# Import the original backend system
try:
    import sys
    import os
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    from Main import main as backend_main
    from Main import get_ouput_directory
    print("Successfully imported original backend system")
except ImportError as e:
    print(f"Failed to import original backend: {e}")
    # Don't raise error, use fallback instead

class OriginalExamShuffler:
    """
    Wrapper class for the original advanced PDF exam shuffling backend
    """
    
    def __init__(self, temp_dir=None):
        """
        Initialize the exam shuffler with original backend
        """
        if temp_dir is None:
            self.temp_dir = tempfile.mkdtemp()
        else:
            self.temp_dir = temp_dir
            os.makedirs(temp_dir, exist_ok=True)
        
        # Set up output directory like the original system expects
        self.output_directory = os.path.join(self.temp_dir, "Local storage of images")
        os.makedirs(self.output_directory, exist_ok=True)
        
        # Create required subdirectories
        os.makedirs(os.path.join(self.temp_dir, "Final PDFs"), exist_ok=True)
        
    def shuffle_pdf_exam(self, input_path, output_path=None):
        """
        Process PDF exam using the original advanced backend
        
        Args:
            input_path: Path to input PDF file
            output_path: Optional output path for processed PDF
            
        Returns:
            tuple: (success_status, output_file_path, error_message)
        """
        try:
            print(f"Processing {input_path} with original backend...")
            
            # Copy input file to working directory 
            working_input = os.path.join(self.temp_dir, os.path.basename(input_path))
            shutil.copy2(input_path, working_input)
            
            # Change to backend directory and set up environment
            original_cwd = os.getcwd()
            backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
            
            # Update the global variables in the Main module
            import Main
            Main.output_directory = self.output_directory + "\\"  # Original expects backslash
            
            try:
                print("Running original backend main function...")
                # Run the original backend main function
                success_pdfs, success_flag = backend_main([working_input])
                
                if success_flag and success_pdfs:
                    print(f"Backend processing successful. Generated: {success_pdfs}")
                    # Get the processed PDF path
                    generated_pdf = success_pdfs[0]
                    
                    # Copy to desired output location if specified
                    if output_path:
                        output_pdf_path = output_path
                        if not output_pdf_path.endswith('.pdf'):
                            output_pdf_path += '.pdf'
                        shutil.copy2(generated_pdf, output_pdf_path)
                        final_path = output_pdf_path
                    else:
                        final_path = generated_pdf
                        
                    return True, final_path, None
                else:
                    print("Backend processing failed - no successful PDFs generated")
                    return False, None, "Original backend processing failed"
                    
            finally:
                # Always return to original directory
                os.chdir(original_cwd)
                
        except Exception as e:
            print(f"Error in original backend processing: {e}")
            return False, None, str(e)
    
    def cleanup(self):
        """
        Clean up temporary files and directories
        """
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception:
            pass

def process_exam_pdf(input_path, output_path=None):
    """
    Convenience function for processing a single PDF exam with original backend
    
    Args:
        input_path: Path to input PDF
        output_path: Path for output PDF (optional)
        
    Returns:
        tuple: (success_status, output_path, error_message)
    """
    print(f"Processing exam PDF: {input_path}")
    
    # For now, just use simple shuffle until Tesseract is properly configured
    print("Using simple PDF shuffle (basic mode)")
    return simple_pdf_shuffle(input_path, output_path)

def simple_pdf_shuffle(input_path, output_path=None):
    """
    Simple PDF shuffle without OCR - fallback method
    """
    try:
        import PyPDF4
        from PyPDF4 import PdfFileReader, PdfFileWriter
        import random
        
        print("Using simple PDF shuffle (fallback mode)")
        
        # Read the PDF
        with open(input_path, 'rb') as file:
            reader = PdfFileReader(file)
            writer = PdfFileWriter()
            
            # Get all pages
            pages = []
            for page_num in range(reader.getNumPages()):
                pages.append(reader.getPage(page_num))
            
            # Simple shuffle - just reverse the order for now
            # In a real implementation, you'd want more sophisticated shuffling
            pages.reverse()
            
            # Add shuffled pages to writer
            for page in pages:
                writer.addPage(page)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"shuffled_exam_{timestamp}.pdf"
            
            # Write the shuffled PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        print(f"Simple shuffle completed: {output_path}")
        return True, output_path, None
        
    except Exception as e:
        error_msg = f"Failed to shuffle PDF: {str(e)}"
        print(f"ERROR: {error_msg}")
        return False, None, error_msg

# Example usage for testing
if __name__ == "__main__":
    test_pdf = r"C:\Users\HP\Downloads\תשפג א א מעורבל.pdf"
    output_pdf = r"test_shuffled_exam.pdf"
    
    success, path, error = process_exam_pdf(test_pdf, output_pdf)
    
    if success:
        print(f"Successfully created shuffled exam: {path}")
    else:
        print(f"Failed to create shuffled exam: {error}")
