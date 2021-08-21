import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from docx import Document

#TODO: Preprocessing : https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/

# Get all pdf files in corrent directory
all_pdf_files = Path.cwd().glob('*.pdf')

# Loop through all the fetched pdf files
for single_pdf_file in all_pdf_files:

  # Get only the stem name (e.g. test from test.pdf)
  pdf_stem_name = str(single_pdf_file.stem)

  # define the path in which a new folder needs to be created to save the pdf images
  images_save_dir = Path.cwd() / pdf_stem_name
  
  # Create a new folder in which the images and docx files will be saved
  # TODO: Check if folder already exists and if so, just continue instead of overwrite
  Path(images_save_dir).mkdir(parents=True, exist_ok=True)

  # Convert PDF content to images
  pdf_images = convert_from_path(single_pdf_file, 500,output_folder=images_save_dir)

  # Define an array in which to fill the image paths (for later, when we will use is for tesseract)
  saved_images = []
  
  # loop through the fetched images of the pdf
  for i in range(len(pdf_images)):

    # save path
    saved_image_path = f'{images_save_dir}/{i}.jpg'

    # save the image
    pdf_images[i].save(saved_image_path,'JPEG')

    # Add the path of the saved image to saved_images
    saved_images.append(saved_image_path)

  # define an empty string which wil be filled with text from the images
  image_text = ''

  # Loop through the saved images paths
  for saved_image in saved_images:

    # Process each image to string
    processed_image = pytesseract.image_to_string(saved_image)
    processed_image = processed_image[:-1]

    image_text+=processed_image

  document = Document()
  document.add_paragraph(image_text)
  document.save(f'{images_save_dir}/{pdf_stem_name}.docx')