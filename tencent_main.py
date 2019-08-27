import cv2
from tencent_util import search_person
import base64
import datetime

video_capture = cv2.VideoCapture(0)
result_file = open("result.xlsx", "w+", encoding='utf-8')

while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        result_file.close()
        break
    elif key == ord('x'):
        image = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8')
        search_result = search_person(image)
        print(search_result['Results'][0]['Candidates'][0])
        try:
            candidate = search_result['Results'][0]['Candidates'][0]
            if candidate['Score'] > 50:
                print(f"{candidate['PersonId']},{candidate['PersonName']},{datetime.datetime.now()}\n")
                result_file.write(f"{candidate['PersonId']},{candidate['PersonName']},")
                result_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}\n")
                result_file.flush()
            else:
                print("no face detected")
        except TypeError:
            print("no face detected")
