#### [1] 아두이노에서 거리센서 값 받아오기
#### [2] 일정 거리 안으로 차량이 근접하면
#### [3] 차량 전면부 사진 촬영
#### [4] 그 이미지를 input으로 detect.py 실행
#### [5] 해당 결과를 txt 파일에 저장

import cv2
import os, sys, time
import numpy as np
import serial

sys.path.insert(0, os.path.dirname(__file__))
from Model.detect_single import detect, post_process, letter_probs_to_code

cnt = 0
weight = "finalweight.npz" # pre-trained weight file
f = np.load(weight)
param_vals = [f[n] for n in sorted(f.files, key=lambda s: int(s[4:]))]

# some parameter for sensor value
dist_port = "COM4"
dist_bRate = 115200

dist_sr = serial.Serial(dist_port, dist_bRate)

while True:
    # choice = input('If you want to capture images, enter [t]') # keyboard input
    sensor_string = dist_sr.readline()[:-2].decode()
    sensor_string = sensor_string.split(':')[1]
    sensor_string = sensor_string[1:-2]
    sensor_dist = float(sensor_string) # distance from HR-04 sensor

    print("distance:", sensor_dist)

    if sensor_dist != 0.0 and sensor_dist <= 15.0 :
    # if choice == 't':
        imgname = './InputImages/Save.jpg' # setting image file name

        cap = cv2.VideoCapture(1) # open video capture
        ret, frame = cap.read()

        if ret:
            print("Take picture complete!")
            cap.release()
            cv2.imwrite(imgname, frame) # save image file
            print("Save picture complete!")
        else:
            print("Capture fail!")

        # frame = cv2.imread("./InputImages/in10.jpg") # test image

        if frame.shape[2] > 600:
            r = 600. / frame.shape[1]
            dsize = (600, int(frame.shape[0] * r))
            frame = cv2.resize(frame, dsize)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255. # RGB -> BG
        start_time = time.time() # set start time

        for letter_probs in post_process(detect(gray, param_vals)):
            code = letter_probs_to_code(letter_probs)
            code = code.replace(" ", "")  # remove space string

            if code is None:
                pass
            else:
                print(code)

        end_time = time.time()
        print("Detect number plate complete!")
        print("Detect processing time:", end_time - start_time)

        # save number plate detection result => gate directory
        with open('C:\\Users\young\eclipse-workspace\Ver3\\nowEnter.txt', 'w', encoding='euc-kr') as f:
            f.write(code)
            print("Save result in gate complete!")
            f.close()

        # save number plate detection result => intersection directory
        with open('C:\\Users\young\eclipse-workspace\Ver3\intersection_getIn\\nowEnter.txt', 'w', encoding='euc-kr') as f:
            f.write(code)
            print("Save result in intersection complete!")
            f.close()

        # lcd_sr.writelines(code) # write code to LCD

    cnt += 1