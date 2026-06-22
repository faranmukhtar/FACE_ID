import cv2 as cv
import numpy as np
import os
import tkinter as tk
import pickle
import Register
import face_recognition






class app:
    def __init__(self , root):
        self.root = root

        self.home = tk.Frame(root)
        self.loading = tk.Frame(root)
        self.camera = tk.Frame(root)
        self.accessgranted = tk.Frame(root)

        self.build_home()
        # self.build_loading()
        # self.build_camera()
    
    def build_accessgranted(self):
        popup = tk.Toplevel(self.root)
        popup.title("Access Granted")
        popup.geometry("200x200")

    def show_frame(self , frame):
        frame.tkraise()

    def ask_name(self):
        popup = tk.Toplevel(self.root)
        popup.title("Enter Name")
        popup.geometry("200x200")

        tk.Label(popup , text = "Enter your name").pack(pady = 10)
        
        entry = tk.Entry(popup)
        entry.pack()

        def submit():
            name = entry.get()
            popup.destroy()
            Register.Registerface(name)
        
        tk.Button(popup, text="Submit", command=submit).pack(pady=10)

    def login(self):
        result = Register.predict()
        if result != "Unknown":
            self.build_accessgranted()

    def build_home(self):
        self.home.place(relwidth=1 , relheight= 1)
        Heading = tk.Label(self.home , text = "Face ID")
        Heading.pack()
        
        
        reg = tk.Button(self.home, text="register", command=self.ask_name)
        reg.pack()

        login = tk.Button(self.home , text = "Login" , command= self.login)
        login.pack()
        
root = tk.Tk()
root.geometry("400x400")
a = app(root)
root.mainloop()
