import os
import numpy as np
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from Util import *
from tkinter import filedialog
import cv2
from PIL import ImageTk, Image

filetype = (("Image Files", "*.BMP;*.JPG;*.PNG;"), ("All files", "*.*"))

WIDTH, HEIGHT = 400, 300


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
        self.button_list.append((Button(command=self.gammaTransformation, text="GAMMA"), "GAMMA"))

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
        src = cv2.imread(ifile.name, 0)
        print(src.shape)
        self.original_image = cv2.resize(src, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
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

    def gammaTransformation(self):
        gamma = simpledialog.askfloat("Gamma", "Gamma: ", parent=self)
        if gamma is not None and 0.4 <= gamma <= 2.2:
            dest = np.array(255 * (self.original_image / 255) ** gamma, dtype='uint8')
            self.updateImage(convertTkImage(dest), "Gamma Transformation (γ=" + str(gamma) + ")")
        else:
            messagebox.showerror("Error", "0.4 ~ 2.2 범위만 입력해주세요.")

    def onSave(self):
        pass
