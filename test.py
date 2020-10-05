import cv2

from datetime import datetime
import time
# get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End", "File_Name"])

cam_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.destroyAllWindows()

while True:
    _, im0 = cam_capture.read()
    showCrosshair = False
    fromCenter = False
    r = cv2.selectROI("Image", im0, fromCenter, showCrosshair)
    break

path = "video_01"
out = cv2.VideoWriter(("./" + path + ".avi"), cv2.VideoWriter_fourcc(*'XVID'), 24.0, (1280, 720))

while True:
    _, image_frame = cam_capture.read()
    status = 0

    rect_img = image_frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    y = r[1]
    x = r[0]
    h = r[3]
    w = r[2]
    sketcher_rect = rect_img

    gray = cv2.cvtColor(sketcher_rect, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, hierarchy = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_test = cv2.rectangle(image_frame, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2)
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1

        (x, y, w, h) = cv2.boundingRect(contour)

        cv2.putText(image_frame, str(datetime.now()), (1018, 18), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.putText(image_frame, 'Motion Detected', (1018, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        out.write(image_frame)

    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Motion Detection", image_frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1], "File_Name": path}, ignore_index=True)

df.to_excel("Time_Logs_Final.xlsx")

cam_capture.release()
cv2.destroyAllWindows()