#!/bin/bash
# Build script for Render deployment

echo "Installing system dependencies..."
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-heb tesseract-ocr-eng tesseract-ocr-ara poppler-utils libgl1-mesa-glx libglib2.0-0

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting up Tesseract environment..."
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

echo "Testing Tesseract installation..."
tesseract --version

echo "Build completed successfully!"
