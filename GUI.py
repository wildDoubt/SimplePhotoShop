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
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Info", command=self.showInformation)
        filemenu.add_command(label="Open", command=self.onOpen)
        filemenu.add_command(label="Save", command=self.onSave)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        master.config(menu=menubar)

        self.choose = Label(self, text="이미지 파일을 선택해주세요")

        self.image = PhotoImage(file='')
        self.label = Label(image=self.image)
        self.curr_image = None
        self.original_image = None

        self.label.pack()
        self.choose.pack()

        self.button_frame = Frame(master)
        self.button_frame.pack(side=BOTTOM, pady=(0, 20))
        self.button_list = []
        self.initButton()

    def initButton(self):
        self.button_list.append(
            (Button(self.button_frame, command=self.resetImage, text="RESET", width=15), "original"))
        self.button_list.append(
            (Button(self.button_frame, command=self.histogramEqualization, text="HE", width=15), "HE"))
        self.button_list.append(
            (Button(self.button_frame, command=self.negativeTransformation, text="NT", width=15), "NT"))
        self.button_list.append(
            (Button(self.button_frame, command=self.gammaTransformation, text="GAMMA", width=15), "GAMMA"))
        self.button_list.append(
            (Button(self.button_frame, command=self.gaussianBlur, text="GAUSSIAN", width=15), "GAUSSIAN"))
        self.button_list.append((Button(self.button_frame, command=self.medianBlur, text="MEDIAN", width=15), "MEDIAN"))
        self.button_list.append(
            (Button(self.button_frame, command=self.averageBlur, text="AVERAGE", width=15), "AVERAGE"))
        self.button_list.append((Button(self.button_frame, command=self.highBoost, text="HIGHBOOST", width=15), "HB"))
        self.button_list.append((Button(self.button_frame, command=self.canny, text="CANNY", width=15), "CANNY"))

    def resetImage(self):
        self.updateImage(convertTkImage(self.original_image), "Original")
        self.curr_image = self.original_image

    def showAllButton(self):
        for i in range(len(self.button_list)):
            self.button_list[i][0].grid(row=i // 3, column=i % 3)

    def hideAllButton(self):
        for button in self.button_list:
            button[0].forget()

    def onOpen(self):
        ifile = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file', filetype=filetype)
        src = autoResize(cv2.imread(ifile.name, 1))

        self.original_image = src
        self.original_image_tk = convertTkImage(self.original_image)
        self.curr_image = self.original_image
        self.label.configure(image=self.original_image_tk)
        self.label.image = self.original_image_tk
        self.choose["text"] = "Original"

        self.showAllButton()

    def updateImage(self, image, description):
        self.label.configure(image=image)
        self.label.image = image
        self.choose["text"] = description

    def histogramEqualization(self):
        self.curr_image = cv2.equalizeHist(cv2.cvtColor(self.curr_image, cv2.COLOR_BGR2GRAY))
        self.updateImage(convertTkImage(self.curr_image), "Histogram Equalization")

        # 컬러 안 바꿔주면 에러 발생
        self.curr_image = cv2.cvtColor(self.curr_image, cv2.COLOR_GRAY2BGR)

    def negativeTransformation(self):
        self.curr_image = 255 - self.curr_image
        self.updateImage(convertTkImage(self.curr_image), "Negative Transformation")

    def gammaTransformation(self):
        gamma = simpledialog.askfloat("Gamma", "γ 값을 입력해주세요.", parent=self)

        if gamma is None:
            return

        if 0.4 <= gamma <= 2.2:
            self.curr_image = np.array(255 * (self.curr_image / 255) ** gamma, dtype='uint8')
            self.updateImage(convertTkImage(self.curr_image), "Gamma Transformation (γ=" + str(gamma) + ")")
        else:
            messagebox.showinfo("Error", "0.4 ~ 2.2 범위만 입력해주세요.")

    def gaussianBlur(self):
        size = simpledialog.askinteger("Mask size", "마스크 사이즈를 입력해주세요.", parent=self)
        if size is None:
            return

        self.curr_image = cv2.GaussianBlur(self.curr_image, (size, size), 0)
        self.updateImage(
            convertTkImage(self.curr_image),
            "Gaussian Filtering (mask size=" + str(size) + " X " + str(size) + ")"
        )

    def medianBlur(self):
        size = simpledialog.askinteger("Mask size", "마스크 사이즈를 입력해주세요.", parent=self)
        if size is None:
            return

        self.curr_image = cv2.medianBlur(self.curr_image, size)
        self.updateImage(
            convertTkImage(self.curr_image),
            "Median Filtering (mask size=" + str(size) + " X " + str(size) + ")"
        )

    def averageBlur(self):
        size = simpledialog.askinteger("Mask size", "마스크 사이즈를 입력해주세요.", parent=self)
        if size is None:
            return

        self.curr_image = cv2.blur(self.curr_image, (size, size))
        self.updateImage(
            convertTkImage(self.curr_image),
            "Average Filtering (mask size=" + str(size) + " X " + str(size) + ")"
        )

    def highBoost(self):
        A = simpledialog.askfloat("A value", "A값을 입력해주세요.", parent=self)
        if A is None:
            return
        option = simpledialog.askinteger("Option", "옵션을 선택하세요.", parent=self)
        if option is None:
            return

        mask = getSharpeningMask(A, option)
        self.curr_image = cv2.filter2D(self.curr_image, -1, mask)
        self.updateImage(
            convertTkImage(self.curr_image),
            "High Boost Filter (A=" + str(A) + ", option=" + str(option) + ")")

    def canny(self):
        self.curr_image = cv2.Canny(self.curr_image, 50, 150)
        self.updateImage(
            convertTkImage(self.curr_image),
            "Canny Operation"
        )

    def showInformation(self):
        messagebox.showinfo("Simple Photoshop", "Opencv 라이브러리를 활용한 이미지 프로세싱 프로그램입니다.")
        pass

    def onSave(self):
        if self.curr_image is None:
            messagebox.showinfo("이미지 없음", "이미지를 먼저 선택해주세요.")
            return
        file = filedialog.asksaveasfile(parent=self,
                                        mode='w',
                                        title="Choose a directory",
                                        filetype=filetype,
                                        initialfile="*.png")
        if file is None:
            return
        cv2.imwrite(file.name, self.curr_image)
        messagebox.showinfo("저장 완료", "성공적으로 저장되었습니다.")
        file.close()
