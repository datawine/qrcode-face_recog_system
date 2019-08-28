# qrcode-face_recog_system
an experimental system for signing in using qrcode or face_recog_system using tencent cloud API.

## prereq

- Use anaconda to manage packages because opencv installation is tricky on Windows(my platform).

- Use `conda env create -f environment.yml` to install the environment, it may take for a while depending on the network speed.

- Need stable network connection.

## usage

- For detection, use `conda activate face_recognition` to activate the environment and run `python tencent_main.py` to start the program.

- Click  the`start` button to open webcam and click the `detect` button to sign. If face took matches a picture existing in the library, a message box
will be pop up showing name and student ID of the person. The signing records will be added into a csv file.

- Use `tencent_util.py` to manage people and their face pictures in the library.

- Contact me \<i@minhu.wang\> | Wechat:wmhstephen for `tencent_secret.py` including API key and secret required by tencent cloud API, or generate one by yourself(recommanded) [Tencent Cloud Link](https://cloud.tencent.com/product/facerecognition).


