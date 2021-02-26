from Radar import TextRecognition
import glob

img = []
for i in glob.iglob("D:\\Github Repositories\\Ship-Radar-Image-Data\\static\\uploads\\*.png"):
  img.append(i)

# img = img[:5]
count = 0
for i in img:
    count += 1
    print("-----------------------------------------")
    print("Image:", count)
    Map = TextRecognition(i)
    print(Map)
    print("-----------------------------------------")