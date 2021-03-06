import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
path = 'ImagesAttendance'
images = []
className = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    currImg = cv2.imread(f'{path}/{cl}')
    images.append(currImg)
    className.append(os.path.splitext(cl)[0])
print(className)
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        return encodeList
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        nameList = []
        myDataList = f.readlines()
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entery[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
encodeListKnown = findEncodings(images)
cap = cv2.VideoCapture(0)
while True:
    success , img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    img = cv2.cvtColor(imgS,cv2.COLOR_RGB2BGR)

    facesCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS,facesCurrFrame)
    for encodeFace,faceLoc in zip(encodeCurrFrame,facesCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDic = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDic)
        matchIndex = np.argmin(faceDic)

        if matches[matchIndex]:
            name = className[matchIndex].upper()
            #print(name)
            y2,x2,y1,x1 = faceLoc
            y2, x2, y1, x1 = y2, x2*4, y1*4, x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)
            markAttendance(name)
            
    cv2.imshow("webcam",img)
    cv2.waitKey(1)
#faceLoc = face_recognition.face_locations(imgLucky)[0]
#encodeLucky = face_recognition.face_encodings(imgLucky)[0]
#cv2.rectangle(imgLucky,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(225,0,255),2)

#faceLocTest = face_recognition.face_locations(imgTest)[0]
#encodeTest = face_recognition.face_encodings(imgTest)[0]
#cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(225,0,255),2)

#result = face_recognition.compare_faces([encodeLucky],encodeTest)
#faceDis = face_recognition.face_distance([encodeLucky],encodeTest)