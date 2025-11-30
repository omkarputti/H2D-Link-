import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def get_finger_states(lm):
    # Tip landmarks
    tips = [8, 12, 16, 20]  # index, middle, ring, pinky
    fingers = []

    # For each finger → check if tip is above the lower joint
    for tip in tips:
        if lm[tip].y < lm[tip - 2].y:
            fingers.append(1)   # extended
        else:
            fingers.append(0)   # curled

    # Thumb detection
    if lm[4].x < lm[3].x:
        thumb = 1
    else:
        thumb = 0

    return fingers, thumb


while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "None"

    if result.multi_hand_landmarks:
        handLms = result.multi_hand_landmarks[0]
        lm = handLms.landmark

        fingers, thumb = get_finger_states(lm)
        extended_count = sum(fingers)

        # NEW GESTURE RULES:

        # 1. OPEN PALM = Forward
        if extended_count == 4:
            gesture = "Forward"

        # 2. FIST = Rotate
        elif extended_count == 0 and thumb == 0:
            gesture = "Rotate"

        # 3. PEACE SIGN = Idle
        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
            gesture = "Idle"

        mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, gesture, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)

    cv2.imshow("Gesture Classifier", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
