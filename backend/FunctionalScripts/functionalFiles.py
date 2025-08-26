from PIL import Image
from pdf2image import convert_from_path
import os
from PyPDF4 import PdfFileMerger

import zipfile

from . import editPng

ouput_directory = "Local storage of images\\"



def merge_pdf(arrayPath,nameFile):
    merger = PdfFileMerger()
    for pdf_file in arrayPath:
        # Append PDF files
        merger.append(pdf_file)

    # Write out the merged PDF file_list
    merger.write(nameFile+".pdf")
    merger.close()
def create_zip(files, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            # Get the base name of the file
            base_name = os.path.basename(file)
            # Add the file to the ZIP
            zipf.write(file, arcname=base_name)

    #return zip_filename


#convert .png to .pdf
def png_to_pdf(sourcePath):
    png = Image.open(sourcePath)
    im_1 = png.convert('RGB')
    im_1.save(sourcePath[:-4]+".pdf")
    return sourcePath[:-4]+".pdf"

#Conver .pdf to .png and crop the begin and the end of the page
def pdf_to_png(pathSource, pathDest):
    pages = convert_from_path(pathSource)
    paths = []
    for i, page in enumerate(pages):
        (width, height) = page.size
        crop_box = (0, 0+150, width, height - 150)
        page = page.crop(crop_box)
        # Convert to RGB if needed to avoid PNG save issues
        if page.mode != 'RGB':
            page = page.convert('RGB')
        
        png_path = pathDest + f'page_{i}.png'
        paths.append(png_path)
        
        # Save with explicit parameters to avoid streaming issues
        try:
            page.save(png_path, 'PNG', optimize=True)
        except Exception as e:
            # Fallback: save as JPEG if PNG fails
            jpg_path = pathDest + f'page_{i}.jpg'
            page.save(jpg_path, 'JPEG', quality=95)
            paths[-1] = jpg_path  # Update the path in the list
            
        editPng.cropSpaceEndPng(paths[-1])
    return paths


def delete_files(paths):
    for i in range(len(paths)):
        os.remove(paths[i])

def combineFiles(arrayPath,output_path):
    # Load the images
    images = [Image.open(path) for path in arrayPath]
    # Determine the total size of the combined image
    total_width = max(img.size[0] for img in images)
    total_height = sum(img.size[1] for img in images)

    # Create a new image to store the combined images
    result = Image.new("RGBA", (total_width, total_height))

    # Paste each image into the result
    y_offset = 0
    for img in images:
        result.paste(img, (0, y_offset))
        y_offset += img.size[1]

    # Save the result
    result.save(output_path+'.png')
    return output_path+'.png'


def getFilesPaths():
    return ouput_directory,os.listdir(ouput_directory)

def getOutputDirectoryPath():
    return ouput_directory


def zipPdf(array_paths,zip_path):
    create_zip(array_paths, zip_path)
