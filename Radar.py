from cv2 import cv2
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import keras_ocr
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

pipeline = keras_ocr.pipeline.Pipeline()


def TextRecognition(imgPath):
    image = cv2.imread(imgPath)
    OriginalImg = image

    crop_img1 = image[20:170, 1030:]  # Ship Information
    crop_img2 = image[250:320, 1030:]  # Target Information
    crop_img3 = image[935:1200, 0:200]  # Deep Sea
    crop_img4 = image[0:50, 50:100]  # Range
    crop_img5 = image[80:110, 150:220]  # Stabilized
    crop_img6 = image[80:110, 100:150]  # Mode

    cv2.imwrite("./images/shipInfo.png", crop_img1)
    cv2.imwrite("./images/targetInfo.png", crop_img2)
    cv2.imwrite("./images/deepsea.png", crop_img3)
    cv2.imwrite("./images/range.png", crop_img4)
    cv2.imwrite("./images/stablized.png", crop_img5)
    cv2.imwrite("./images/mode.png", crop_img6)

    images = [keras_ocr.tools.read(url) for url in [
        "./images/mode.png",
        "./images/range.png",
        "./images/stablized.png"
    ]
    ]

    prediction_groups = pipeline.recognize(images)

    fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
    for ax, image, predictions in zip(axs, images, prediction_groups):
        keras_ocr.tools.drawAnnotations(
            image=image, predictions=predictions, ax=ax)

    imgPath1 = "./images/shipInfo.png"
    imgPath2 = "./images/targetInfo.png"
    imgPath3 = "./images/stablized.png"
    imgPath4 = "./images/deepsea.png"

    text1 = pytesseract.image_to_string(
        Image.open(imgPath1),
        config=tessdata_dir_config)
    text2 = pytesseract.image_to_string(
        Image.open(imgPath2),
        config=tessdata_dir_config)
    text3 = pytesseract.image_to_string(
        Image.open(imgPath3),
        config=tessdata_dir_config)
    text4 = pytesseract.image_to_string(
        Image.open(imgPath4),
        config=tessdata_dir_config)

    def ShipInformation(text):
        text = text.split("\n")
        HDG = text[0].split(" ")[-1]
        if(len(HDG) < 2):
            HDG = ' '.join(text[0].split(" ")[-2:])

        SPD = ' '.join(text[1].split(" ")[-2:])
        if(len(SPD) < 2):
            SPD = ' '.join(text[1].split(" ")[-3:])

        COG = text[2].split(" ")[-1]
        if(len(COG) < 2):
            COG = ' '.join(text[2].split(" ")[-2:])

        SOG = ' '.join(text[3].split(" ")[-2:])
        if(len(SOG) < 2):
            SOG = ' '.join(text[3].split(" ")[-3:])

        UTC = [" ".join(time.split(" ")[1:]) for time in text if(
            time and time[0] == "U")][0]
        shipInfo = {"HDG": HDG, "SPD": SPD, "COG": COG, "SOG": SOG, "UTC": UTC}
        return shipInfo

    def TargetInformation(text):
        text = text.split("\n")
        vector = ' '.join(text[0].split(" ")[1:])
        posn = ', Time '.join(text[2].split(" ")[2:-1])
        targetInfo = {"Vector": vector, "Past Posn": posn}
        return targetInfo

    def Stabilized(text):
        text = text.split("\n")[0]
        stable = {"Stabilized": text}
        return stable

    def ModeDisp():
        mode = prediction_groups[0][0][0]+" "+prediction_groups[0][1][0]
        Mode = {"Mode": mode}
        return Mode

    def BarMode(text):
        t = text.split("\n")
        while("" in t):
            t.remove("")
        while(" " in t):
            t.remove(" ")

        sea = t[1].split(" ")[-1]
        rain = t[2].split(" ")[-1]
        tune = t[3].split(" ")[-1]
        modes = {"Sea": sea, "Rain": rain, "Tune": tune}
        return modes

    def Range():
        toprange = prediction_groups[1][0][0]
        Range = {"Range": toprange}
        return Range

    image = OriginalImg

    def crop_bars(x, xh, y, yh, name):
        crop_img = image[x: xh, y: yh]
        name = "./images/" + name + ".png"
        cv2.imwrite(name, crop_img)

    crop_bars(940, 950, 62, 113, "GainCrop")  # Gain Bar Image
    crop_bars(960, 970, 62, 113, "SeaCrop")  # Sea Bar Image
    crop_bars(980, 990, 62, 113, "RainCrop")  # Rain Bar Image
    crop_bars(1000, 1010, 62, 113, "TuneCrop")  # Tune Bar Image

    def bar_percentage(cropped_image):
        white = [248, 248, 248]  # RGB
        diff = 30
        boundaries = [([white[2]-diff, white[1]-diff, white[0]-diff],
                    [white[2]+diff, white[1]+diff, white[0]+diff])]
        for (lower, _) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array([255, 255, 255], dtype=np.uint8)
            mask = cv2.inRange(cropped_image, lower, upper)
            ratio_white = cv2.countNonZero(mask)/(cropped_image.size/3)
            return(np.round(ratio_white*100, 2))

    def ShowBars():
        Gain_percentage_crop = cv2.imread('./images/GainCrop.png')
        Sea_percentage_crop = cv2.imread('./images/SeaCrop.png')
        Rain_percentage_crop = cv2.imread('./images/RainCrop.png')
        Tune_percentage_crop = cv2.imread('./images/TuneCrop.png')
        value = BarMode(text4)
        Bars = {"Gain": str(bar_percentage(Gain_percentage_crop))+"%",
                "Sea": str(bar_percentage(Sea_percentage_crop))+"%",
                "Sea Mode": value['Sea'],
                "Rain": str(bar_percentage(Rain_percentage_crop))+"%",
                "Rain Mode": value['Rain'],
                "Tune": str(bar_percentage(Tune_percentage_crop))+"%",
                "Tune Mode": value["Tune"]
                }
        return Bars

    def GetValues():
        Map = {}
        res1 = ShipInformation(text1)
        res2 = TargetInformation(text2)
        res3 = Stabilized(text3)
        res4 = ModeDisp()
        res5 = Range()
        res6 = ShowBars()
        Map.update(res1)
        Map.update(res2)
        Map.update(res3)
        Map.update(res4)
        Map.update(res5)
        Map.update(res6)
        return Map
    Map = GetValues()
    return Map
