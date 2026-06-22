import cv2 as cv
import numpy as np
import os
import tkinter as tk
import Register


class app:
    def __init__(self , root):
        self.root = root

        self.home = tk.Frame(root)
        self.loading = tk.Frame(root)
        self.camera = tk.Frame(root)

        self.build_home()
        self.build_loading()
        self.build_camera()

        self.show_frame(self.home)

    def show_frame(self , frame):
        frame.tkraise()
    
    def build_home(self):
        self.home.place(relwidth=1 , relheight= 1)

        tk.Button(self.home , text = "New face" , command = self)
