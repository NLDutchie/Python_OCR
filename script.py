import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
from PIL import Image

# Create a temp folder to save temp images in
with tempfile.TemporaryDirectory() as temp_dir:
  pdfFiles = Path.cwd().glob('*.pdf')
  for pdfFile in pdfFiles:
    stemName = str(pdfFile.stem)
    fileName = str(pdfFile.name)
    saveDir = Path.cwd() / stemName
    Path(saveDir).mkdir(parents=True, exist_ok=True)

    # Convert PDF contents to pages
    pages = convert_from_path(fileName, 500,poppler_path=r"D:\poppler-21.03.0\Library\bin",output_folder=temp_dir)
    
    # Create an array of temp images
    temp_images = []

    # Go through the pages
    for i in range(len(pages)):
      image_path = f'{temp_dir}/{i}.jpg'
      pages[i].save(image_path, 'JPEG')
      temp_images.append(image_path)
    # read images into pillow.Image
    imgs = list(map(Image.open, temp_images))
    # find minimum width of images
    min_img_width = min(i.width for i in imgs)
    # find total height of all images
    total_height = 0
    for i, img in enumerate(imgs):
        total_height += imgs[i].height
    # create new image object with width and total height
    merged_image = Image.new(imgs[0].mode, (min_img_width, total_height))
    # paste images together one by one
    y = 0
    for img in imgs:
        merged_image.paste(img, (0, y))
        y += img.height
    # save merged image
    savedImagePath = f'{saveDir}/{stemName}.jpg'
    merged_image.save(savedImagePath, 'JPEG')
    
    print(pytesseract.image_to_string(savedImagePath))
