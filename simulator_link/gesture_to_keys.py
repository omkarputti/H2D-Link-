import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"

import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=r"SymbolDatabase\.GetPrototype\(\) is deprecated.*"
)

import cv2
import mediapipe as mp
from pynput.keyboard import Controller

# ----------------------------------------------------
# WINDOWS CAMERA INITIALIZATION
# ----------------------------------------------------
cap = cv2.VideoCapture(0)   # Windows default backend
if not cap.isOpened():
    raise Exception("Camera failed to open on Windows.")

print("Camera opened successfully on Windows")

keyboard = Controller()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
mp_draw = mp.solutions.drawing_utils


def get_finger_states(lm):
    tips = [8, 12, 16, 20]
    fingers = []

    for tip in tips:
        if lm[tip].y < lm[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    thumb = 1 if lm[4].x < lm[3].x else 0
    return fingers, thumb


last_gesture = "None"


def press(key):
    keyboard.press(key)
    keyboard.release(key)


# ----------------------------------------------------
# MAIN LOOP (WINDOWS-SAFE)
# ----------------------------------------------------
while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        continue  # retry instead of exiting

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "None"

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark
        fingers, thumb = get_finger_states(lm)
        ext = sum(fingers)

        if ext == 4:
            gesture = "Forward"
        elif ext == 0 and thumb == 0:
            gesture = "Rotate"
        elif fingers[0] == 1 and fingers[1] == 1:
            gesture = "Idle"

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, gesture, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Gesture → Keys", frame)

    key = cv2.waitKey(1)
    if key == 27: #ESC to exit
        break  

    if gesture != last_gesture:
        if gesture == "Forward":
            press('w')
        elif gesture == "Rotate":
            press('q')
        elif gesture == "Idle":
            press('s')

    last_gesture = gesture

cap.release()
cv2.destroyAllWindows()
