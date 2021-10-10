import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime


video_capture = cv2.VideoCapture(0)

santa_image = face_recognition.load_image_file("santa.jpg")
santa_face_encoding = face_recognition.face_encodings(santa_image)[0]

earth_image = face_recognition.load_image_file("earth.jpg")
earth_face_encoding = face_recognition.face_encodings(earth_image)[0]

plub_image = face_recognition.load_image_file("plub.jpg")
plub_face_encoding = face_recognition.face_encodings(plub_image)[0]


known_face_encodings = [
    santa_face_encoding,
    earth_face_encoding,
    plub_face_encoding
]
known_face_names = [
    "Wachirawit Piyaprapapan",
    "Punnawat Piyaoranrut",
    "Jiraplus Jantarapong"
]


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

Attendance = open('Attendance.csv', 'r+')
Attendance.truncate(0)
Attendance.writelines(["Name,Date,Time"])
Attendance.close()

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now =  datetime.now()
            dString = now.strftime('%D')
            tString = now.strftime('%H:%M')
            f.writelines(f'\n{name},{dString},{tString}')
        

while True:

    ret, frame = video_capture.read() 

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

 
    rgb_small_frame = small_frame[:, :, ::-1]

    
    if process_this_frame:
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    ##process_this_frame = not process_this_frame



    for (top, right, bottom, left), name in zip(face_locations, face_names):

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 225, 0), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 225, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        markAttendance(name)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()