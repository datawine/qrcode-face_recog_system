import face_recognition
import cv2
import numpy as np
from namelist_util import *
import datetime
from PIL import ImageFont, ImageDraw, Image

# this program is derived from face_recognition/facerec_from_webcam_faster.py

def init():
    # init namelist
    namelist = import_namelist()

    # init cam
    video_capture = cv2.VideoCapture(0)

    # init face data
    known_face_encodings = []
    known_face_names = []
    for stu_id in namelist.keys():
        if stu_id.find('x') != -1:
            # stu id contains x is for test use
            continue

        test_image = face_recognition.load_image_file("img/" + stu_id + ".jpg")
        test_face_encoding =  face_recognition.face_encodings(test_image)[0]
        known_face_encodings.append(test_face_encoding)
        known_face_names.append(stu_id)

    return namelist, video_capture, known_face_encodings, known_face_names

if  __name__ == '__main__':

    namelist, video_capture, known_face_encodings, known_face_names = init()

    # Initialize some variables
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
            stu_id = ""
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    stu_id = known_face_names[best_match_index]
                    name = namelist[stu_id]["name"]

                face_names.append(name)
                # if not signed in, sign in onto sheet
                if (stu_id in namelist) and namelist[stu_id]["time"] == "None":
                    cur_time = datetime.datetime.now()
                    namelist[stu_id]["time"] = cur_time.strftime("%Y-%m-%d %H:%M:%S")
                    print("updating: ", stu_id, namelist[stu_id]["name"], cur_time)

        process_this_frame = not process_this_frame


        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # show name on cam
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            font = ImageFont.truetype("simhei.ttf", 32, encoding="utf-8")
            frame_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame_pil)
            draw.text((left + 6, bottom - 30), name, font=font, fill=(255, 255, 255))
            frame = np.array(frame_pil)

            # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(namelist)
            export_signin_result(namelist)
            break

    video_capture.release()
    cv2.destroyAllWindows()
