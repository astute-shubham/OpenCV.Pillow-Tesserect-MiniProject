#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.

# In[ ]:


import zipfile
import PIL
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
def newspaper_info(link_zip):
    newspaper = []
    with zipfile.PyZipFile(link_zip) as archive:
        for entry in archive.infolist():
            with archive.open(entry) as file:
                page_info = {}
                page_info['file_name'] = entry.filename
                print('Analysing in {}'.format(entry.filename))

                img = Image.open(file)
                page_info['image'] = img

                img = img.convert('L')
                page_info['text'] = pytesseract.image_to_string(img)

                open_cv_image = np.array(img.convert('RGB'))
                open_cv_image = open_cv_image[:, :, ::-1].copy()
                gray = cv.cvtColor(open_cv_image, cv.COLOR_BGR2GRAY)
                page_info['gray'] = gray
                # page_info['bounding_boxes'] = face_cascade.detectMultiScale(gray, 1.35).tolist()

            newspaper.append(page_info)
    print('Analysing fiinished!')
    return newspaper
def text_search_and_img_display(text_search, level_dectection, newspaper):
    for page in newspaper:
        bounding_boxes = list(face_cascade.detectMultiScale(page['gray'], level_dectection, 5))
        if text_search in page['text']:
            print('Results found in file {}'.format(page['file_name']))
            if len(bounding_boxes) == 0:
                print('But there were no faces in that file!')
            else:
                rows_size = (len(bounding_boxes) - 1)//5 + 1
                first_image = page['image'].crop((0, 0, 100, 100))
                first_image.thumbnail((100, 100))
                contact_sheet= Image.new(first_image.mode, (first_image.width*5,first_image.height*rows_size))
                x=0
                y=0

                for iboxes in bounding_boxes:
                    box = iboxes @ np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
                    img = page['image'].crop(box)
                    img.thumbnail((100, 100), Image.ANTIALIAS)
                    contact_sheet.paste(img, (x, y) )
                    
                    if x+first_image.width == contact_sheet.width:
                        x=0
                        y=y+first_image.height
                    else:
                        x=x+first_image.width

                display(contact_sheet)
    return None
my_newspaper = newspaper_info('./readonly/small_img.zip')
text_search_and_img_display('Christophe', 1.3, my_newspaper)
def newspaper_info(link_zip):
    newspaper = []
    with zipfile.PyZipFile(link_zip) as archive:
        for entry in archive.infolist():
            with archive.open(entry) as file:
                page_info = {}
                page_info['file_name'] = entry.filename
                print('Analysing in {}'.format(entry.filename))

                img = Image.open(file)
                page_info['image'] = img

                img = img.convert('L')
                page_info['text'] = pytesseract.image_to_string(img)

                open_cv_image = np.array(img.convert('RGB'))
                open_cv_image = open_cv_image[:, :, ::-1].copy()
                gray = cv.cvtColor(open_cv_image, cv.COLOR_BGR2GRAY)
                page_info['gray'] = gray
                # page_info['bounding_boxes'] = face_cascade.detectMultiScale(gray, 1.35).tolist()

            newspaper.append(page_info)
    print('Analysing fiinished!')
    return newspaper
def text_search_and_img_display(text_search, level_dectection, newspaper):
    for page in newspaper:
        bounding_boxes = list(face_cascade.detectMultiScale(page['gray'], level_dectection, 5))
        if text_search in page['text']:
            print('Results found in file {}'.format(page['file_name']))
            if len(bounding_boxes) == 0:
                print('But there were no faces in that file!')
            else:
                rows_size = (len(bounding_boxes) - 1)//5 + 1
                first_image = page['image'].crop((0, 0, 100, 100))
                first_image.thumbnail((100, 100))
                contact_sheet= Image.new(first_image.mode, (first_image.width*5,first_image.height*rows_size))
                x=0
                y=0

                for iboxes in bounding_boxes:
                    box = iboxes @ np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
                    img = page['image'].crop(box)
                    img.thumbnail((100, 100), Image.ANTIALIAS)
                    contact_sheet.paste(img, (x, y) )
                    
                    if x+first_image.width == contact_sheet.width:
                        x=0
                        y=y+first_image.height
                    else:
                        x=x+first_image.width

                display(contact_sheet)
    return None
my_newspaper = newspaper_info('./readonly/small_img.zip')
text_search_and_img_display('Christophe', 1.3, my_newspaper)
my_newspaper2 = newspaper_info('./readonly/images.zip')
text_search_and_img_display('Mark', 1.3, my_newspaper2)


# In[ ]:




