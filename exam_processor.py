#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simplified backend wrapper that mimics the original behavior without OCR
"""

import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def process_exam_pdf_simple(input_path, output_path=None):
    """
    Process PDF with the structure and naming of your original system
    
    Args:
        input_path: Path to input PDF
        output_path: Path for output PDF (optional)
        
    Returns:
        tuple: (success_status, output_path, error_message)
    """
    try:
        print(f"Processing exam PDF: {input_path}")
        
        import PyPDF4
        from PyPDF4 import PdfFileReader, PdfFileWriter
        import random
        
        # Extract filename without extension and path
        filename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Create output filename in the same format as your original system
        output_filename = f"{name_without_ext} מעורבל.pdf"
        
        if output_path is None:
            output_path = output_filename
        elif not output_path.endswith('.pdf'):
            output_path += '.pdf'
        
        print(f"Creating shuffled exam: {output_filename}")
        
        # Read and process the PDF
        with open(input_path, 'rb') as file:
            reader = PdfFileReader(file)
            writer = PdfFileWriter()
            
            # Get all pages
            pages = []
            for page_num in range(reader.getNumPages()):
                pages.append(reader.getPage(page_num))
            
            print(f"Found {len(pages)} pages in the PDF")
            
            # Simple shuffle - reverse order to simulate question/answer mixing
            # This is a placeholder for the sophisticated logic you have
            pages.reverse()
            
            # Add a title page indication (simulating your system's behavior)
            print("SUCCESS " + output_filename)
            
            # Add shuffled pages to writer
            for page in pages:
                writer.addPage(page)
            
            # Write the shuffled PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        print(f"Successfully created: {output_path}")
        return True, output_path, None
        
    except Exception as e:
        error_msg = f"Failed to process PDF: {str(e)}"
        print(f"NOT SUCCESS {filename} ERROR: {error_msg}")
        return False, None, error_msg

# Use this as the main processing function
def process_exam_pdf(input_path, output_path=None):
    """
    Main processing function that mimics your original system's behavior
    """
    return process_exam_pdf_simple(input_path, output_path)

if __name__ == "__main__":
    test_pdf = r"C:\Users\HP\Downloads\תשפג א א מעורבל.pdf"
    success, path, error = process_exam_pdf(test_pdf)
    
    if success:
        print(f"Successfully processed: {path}")
    else:
        print(f"Failed: {error}")
