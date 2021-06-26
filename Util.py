from tkinter import *
import cv2
from PIL import ImageTk, Image

WIDTH, HEIGHT = 500, 500


def convertTkImage(src):
    result = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(result)
    return ImageTk.PhotoImage(image=img)


def autoResize(image):
    width = image.shape[1]
    height = image.shape[0]
    ratio = (width / WIDTH, height / HEIGHT)

    if ratio[0] < 1 and ratio[1] < 1:
        return image
    else:
        if ratio[0] > ratio[1]:
            arg = 1 / ratio[0]
        else:
            arg = 1 / ratio[1]
        return cv2.resize(image, dsize=(0, 0), fx=arg, fy=arg, interpolation=cv2.INTER_AREA)
