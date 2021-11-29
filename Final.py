import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
from tkinter import *
from tkinter import ttk


studentData = open('data606.csv', 'r+', encoding='UTF-8')
csv_Reader = csv.reader(studentData, delimiter = ',')  

video_capture = cv2.VideoCapture(0)
known_face_encodings = []
known_face_names = []


##ใส่YEsหลังใส่รูป
print('load picture . . .')
for row in csv_Reader:
    iNumber, Name, Grade, Class, Number, Pic = row   
    if Pic == "Yes":
        temp = face_recognition.load_image_file('attendancePicture\%s.jpg' %iNumber)
        known_face_encodings.append(face_recognition.face_encodings(temp)[0])
        known_face_names.append(iNumber)
        print('Load',iNumber, Name, Grade, Class, Number, Pic)
print('finish encodings')


now =  datetime.now()
todayDate = now.strftime("%d_%m_%Y")
Attendance = open('Attendance_%s.csv' %todayDate, 'w')
Attendance.writelines(["Name, iNumber, Grade, Class, Number, Date, Time"])
Attendance.close()


def markAttendance(Name, iNumber, Grade, Class, Number):
    with open('Attendance_%s.csv' %todayDate,'r+', encoding='UTF-8') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if Name not in nameList:
            dString = now.strftime('%D')
            tString = now.strftime('%H:%M')
            f.writelines(f'\n{Name},{iNumber},{Grade},{Class},{Number},{dString},{tString}')
            tv.insert('', 'end', values=(Name, iNumber, Grade, Class, Number, dString, tString))
        
app = Tk()
app.title('Test')
app.geometry('500x1000')

tv = ttk.Treeview(app, columns=('col_1', 'col_2', 'col_3','col_4', 'col_5', 'col_6', 'col_7'), show='headings')
tv.column('col_1', minwidth=0, width=175)
tv.column('col_2', minwidth=0, width=80)
tv.column('col_3', minwidth=0, width=50)
tv.column('col_4', minwidth=0, width=50)
tv.column('col_5', minwidth=0, width=50)
tv.column('col_6', minwidth=0, width=75)
tv.column('col_7', minwidth=0, width=55)

tv.heading('col_1', text='ชื่อ  นามสกุล')
tv.heading('col_2', text='เลขประจำตัว')
tv.heading('col_3', text='ชั้น')
tv.heading('col_4', text='ห้อง')
tv.heading('col_5', text='เลขที่')
tv.heading('col_6', text='วัน')
tv.heading('col_7', text='เวลา')
##Name, iNumber, Grade, Class, Number, Date, Time
tv.pack()
print ('Packed the window')


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:

    ret, frame = video_capture.read() 

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

 
    rgb_small_frame = small_frame[:, :, ::-1]

    
    if process_this_frame:
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            
            ##matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) 
            ##find min number of all list of face_distance and gives us the indices of that
            facePercent = 1-face_distances[best_match_index]
            ##face_distances[best_match_index] คือหาตำแหน่งที่ best_match_index ใน face_distance
            if facePercent>= 0.5   :
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    ##Showing
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 225, 0), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 225, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    cv2.imshow('Video', frame)

    Him = ''.join(str(x) for x in face_names)
    studentData = open('data606.csv', 'r+', encoding='UTF-8')
    csv_Reader = csv.reader(studentData, delimiter = ',')

    for row in csv_Reader:
        iNumber, Name, Grade, Class, Number, Pic = row   
        if iNumber == Him:
            markAttendance(Name, iNumber, Grade, Class, Number)



    Attendance = open('Attendance_%s.csv' %todayDate, 'r+', encoding='UTF-8')
    AttendanceReader = csv.reader(Attendance, delimiter = ',')
    AttendanceWriter = csv.writer(Attendance, delimiter = ',')
    next(AttendanceReader)   

    AttendanceReader_list = list(AttendanceReader)

    app.update()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()



