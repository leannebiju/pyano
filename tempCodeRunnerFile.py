import cv2
import mediapipe as mp
import pygame.mixer as play

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

play.init()
notes = {
    "C": play.Sound("notes/C3.wav"),
    "D": play.Sound("notes/D3.wav"),
    "E": play.Sound("notes/E3.wav"),
    "F": play.Sound("notes/F3.wav"),
    "G": play.Sound("notes/G3.wav"),
    "A": play.Sound("notes/A3.wav"),
    "B": play.Sound("notes/B3.wav")
}

cap = cv2.VideoCapture(0)
screen_width = int(cap.get(3))
screen_height = int(cap.get(4))

white_keys = ["C", "D", "E", "F", "G", "A", "B"]
white_key_width = screen_width // 7
white_key_height = screen_height // 2
active_keys = set()

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    pressed_keys = set()

    for i, key in enumerate(white_keys):
        x_min = i * white_key_width
        x_max = x_min + white_key_width
        key_color = (255, 200, 200) if key in active_keys else (255, 255, 255)
        cv2.rectangle(frame, (x_min, 0), (x_max, white_key_height), key_color, -1)
        cv2.rectangle(frame, (x_min, 0), (x_max, white_key_height), (0, 0, 0), 2)
        cv2.putText(frame, key + "3", (x_min + 20, white_key_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            
            for id in [4, 8, 12, 16, 20]:
                lm = hand_landmarks.landmark[id]
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if cy < white_key_height:
                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                    for i, key in enumerate(white_keys):
                        x_min = i * white_key_width
                        x_max = x_min + white_key_width
                        if x_min <= cx < x_max:
                            pressed_keys.add(key)
                            if key not in active_keys:
                                print(f"Playing {key}3")
                                notes[key].play()
                            break

    for key in active_keys - pressed_keys:
        notes[key].stop()

    active_keys = pressed_keys

    cv2.imshow("Pyano", frame)

    if cv2.waitKey(1) == 13 or cv2.getWindowProperty('Pyano', cv2.WND_PROP_VISIBLE) == 0:
        break

cap.release()
cv2.destroyAllWindows()
