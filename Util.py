from tkinter import *
import cv2
from PIL import ImageTk, Image

def convertTkImage(src):
    result = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(result)
    return ImageTk.PhotoImage(image=img)
