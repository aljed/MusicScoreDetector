import PIL.Image as im
from pdf2image import convert_from_path
import imageio
import _elementtree
import os

SOURCE = 'nuty'
DESTINATION = 'pictures'

def picturify():
    files = os.listdir(SOURCE)
    for file in files:
        pages = convert_from_path(SOURCE+'\\'+file)
        for i, page in enumerate(pages):
            print(file)
            page.save(f"{DESTINATION}\\{file}_{i}.jpg", 'JPEG')

def normalize():
    files = os.listdir(DESTINATION)
    for file in files:
        image = im.open(DESTINATION+'\\'+file, mode='r')
        im2 = image.resize((840,593*2))
        im2.save(DESTINATION+'_resized\\'+file, 'JPEG')

picturify()
normalize()