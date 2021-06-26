from tkinter import *
import cv2
from PIL import ImageTk, Image
import numpy as np

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


def getSharpeningMask(A, option):
    # 마스크 사이즈는 3으로 고정
    if option == 1:
        mask = np.array([[0, -1, 0], [-1, 4 + A, -1], [0, -1, 0]])
    else:
        mask = np.ones((3, 3))
        mask = -mask
        mask[1][1] = A + 8
    return mask
