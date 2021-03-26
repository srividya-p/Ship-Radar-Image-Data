'''
This file is solely for Testing purpose.
Add the path of folder containing radar images
'''
from Radar import TextRecognition
import glob

# Add your path here
path = "D:\\Github Repositories\\Ship-Radar-Image-Data\\static\\uploads\\*.png"
img = []
for i in glob.iglob(path):
    img.append(i)

count = 0
for i in img:
    count += 1
    print("-----------------------------------------")
    print("Image:", count)
    Map = TextRecognition(i)
    print(Map)
    print("-----------------------------------------")