# qrcode-face_recog_system
an experimental system for signing in using qrcode or face_recog_system

## prereq

- this program is intended for mac or linux
- pip3 install face_recognition, openpyxl, Pillow

## usage

- put stu_id.jpg in folder img, for example 2019214553.jpg
- fill namelist.xlsx with student name and student id (if an id contains 'x' means its for test, and wont be change)

- use command `python3 main.py` (this will ask the permission to camera)
- sign in update will be shown in terminal output and updated in excel

- the result is shown in output.xlsx

- for the convinience, i put namelist.xlsx and output.xlsx on github, but i wont put my pic on github too :)