import cv2 as cv
import numpy as np
import os
import tkinter as tk
import pickle
import time
import face_recognition
import sys
import shutil

def merge_folders(source , target):
    os.makedirs(target , exist_ok= True)
    files = os.listdir(source)
    existing = len(os.listdir(target))
    for i , file in enumerate(files):
        src = os.path.join(source , file)
        new_name = f"{os.path.basename(target)}_{existing + i}.jpg"
        dst = os.path.join(target , new_name)
        shutil.move(src , dst)
    
    os.rmdir(source)

    print("Merge Completed")



def Registerface():

    BASE = "SAVED_PEOPLE"
    os.makedirs(BASE , exist_ok= True)

    Encodingsfile = "Encodings.pkl"
    Namesfile = "Names.pkl"

    if os.path.exists(Encodingsfile):
        with open(Encodingsfile , 'rb') as f:
            known_face_encodings = pickle.load(f)
    
    else:
        known_face_encodings = []

    if os.path.exists(Namesfile):
        with open(Namesfile , "rb") as f:
            known_names = pickle.load(f)
    else:
        known_names= []

    for person in os.listdir(BASE):
        person_path = os.path.join(BASE , person)
        if not os.path.isdir(person_path):
            continue

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path , img_name)
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 0:
                known_face_encodings.append(encodings[0])
                known_names.append(person)
            


    captured_encodings = []
    frames = []

    time.sleep(2) 
    sys.stdin.flush()
    name = input("Enter youre name: ")

    path = os.path.join(BASE , name)
    os.makedirs(path , exist_ok= True)



    for i in range(3):
        capture = cv.VideoCapture(0)
        for j in range(10):
            capture.read()

        count = 1
        while count < 6 :
            isTrue , frame = capture.read()
            if not isTrue:
                continue

            
            rgb = cv.cvtColor(frame , cv.COLOR_BGR2RGB)

            faceloc = face_recognition.face_locations(rgb)
            
            cropped = 0

            if len(faceloc) > 0:
                top , right , bottom , left = faceloc[0]
                cropped = frame[top:bottom , left:right]
                croppedrgb = cv.cvtColor(cropped , cv.COLOR_BGR2RGB)
                encod = face_recognition.face_encodings(croppedrgb)
              
                cv.rectangle(frame , (left , top) , (right , bottom) , (0,255, 0) , 2)            


            cv.imshow("Face Registration", frame)
            cv.setWindowTitle("Face Registration", ["Please look STRAIGHT....", "Please look LEFT....", "Please look RIGHT...."][i])
            cv.waitKey(1)

           
            if(len(encod) > 0):
                captured_encodings.append(encod[0])
                frames.append(croppedrgb)
                cv.imwrite(f"{path}/{name}_{i}_{count}.jpg", cropped)
                count +=1
            else:
                cv.imshow("Face Registration" , frame)
                cv.waitKey(1)

            time.sleep(0.2)

        capture.release()
        cv.destroyAllWindows()
        time.sleep(1)

    if not captured_encodings:
        print("No faces detected during capture. Try again.")
        exit()


    confirm = 'N'
    if known_face_encodings:
        best_distance = 999
        for enc in captured_encodings:
            distances = face_recognition.face_distance(
            known_face_encodings,
            enc )

            best_match = np.argmin(distances)

            if distances[best_match] < best_distance:
                best_distance = distances[best_match]
                fname = known_names[best_match]

        
        if best_distance < 0.5:
            print(f"Possible match: {fname}")
            print(f'Distance: {best_distance:.3f}')
            confirm = input("Correct? Y/N")

            if confirm.upper() == 'Y':
                target = os.path.join(BASE , fname)
                source = os.path.join(BASE , name)
                merge_folders(source , target)



    if confirm.upper() == 'N':
        print(f"New face saved of {name}")
        known_names.append(name)
        with open("Names.pkl" , "wb") as f:
            pickle.dump(known_names , f)

    known_face_encodings.extend(captured_encodings)
    with open("Encodings.pkl" , "wb") as f:
        pickle.dump(known_face_encodings , f) 


Registerface()