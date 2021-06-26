import os
import numpy as np
from tkinter import *
from Util import *
from tkinter import filedialog
import cv2
from PIL import ImageTk, Image

filetype = (("Image Files", "*.BMP;*.JPG;*.PNG;"), ("All files", "*.*"))

class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        w, h = 650, 650
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        master.title("Mini Photoshop")
        self.pack()

        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.onOpen)
        filemenu.add_command(label="Save", command=self.onSave)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        master.config(menu=menubar)
        self.choose = Label(self, text="이미지 파일을 선택해주세요")

        self.image = PhotoImage(file='')
        self.label = Label(image=self.image)

        self.label.pack()
        self.choose.pack()
        self.button_list = []
        self.initButton()

    def initButton(self):
        self.button_list.append((Button(command=self.resetImage, text="RESET"), "original"))
        self.button_list.append((Button(command=self.histogramEqualization, text="HE"), "HE"))
        self.button_list.append((Button(command=self.negativeTransformation, text="NT"), "NT"))

    def resetImage(self):
        self.updateImage(convertTkImage(self.original_image), "Original")

    def showAllButton(self):
        for button in self.button_list:
            button[0].pack()

    def hideAllButton(self):
        for button in self.button_list:
            button[0].forget()

    def onOpen(self):
        ifile = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file')

        self.original_image = cv2.imread(ifile.name, 0)
        self.original_image_tk = convertTkImage(self.original_image)
        self.label.configure(image=self.original_image_tk)
        self.label.image = self.original_image_tk
        self.choose["text"] = "Original"

        self.showAllButton()

    def updateImage(self, image, description):
        self.label.configure(image=image)
        self.label.image = image
        self.choose["text"] = description

    def histogramEqualization(self):
        dest = cv2.equalizeHist(self.original_image)
        self.updateImage(convertTkImage(dest), "Histogram Equalization")

    def negativeTransformation(self):
        dest = 255 - self.original_image
        self.updateImage(convertTkImage(dest), "Negative Transformation")

    def onSave(self):
        pass
