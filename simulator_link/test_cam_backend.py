import cv2

print("1) Testing V4L2...")
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
print("Opened:", cap.isOpened())
if cap.isOpened():
    ret, frame = cap.read()
    print("V4L2 empty frame:", frame is None)

print("\n2) Testing GStreamer...")
cap2 = cv2.VideoCapture("v4l2src device=/dev/video0 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)
print("Opened:", cap2.isOpened())
if cap2.isOpened():
    ret2, frame2 = cap2.read()
    print("GStreamer empty frame:", frame2 is None)

print("\n3) Testing CAP_ANY...")
cap3 = cv2.VideoCapture(0, cv2.CAP_ANY)
print("Opened:", cap3.isOpened())
if cap3.isOpened():
    ret3, frame3 = cap3.read()
    print("CAP_ANY empty frame:", frame3 is None)
