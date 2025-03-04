import cv2
import mediapipe as mp
import pygame.mixer as play

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

play.init()
notes = {
    "C3": play.Sound("notes/C3.wav"), "D3": play.Sound("notes/D3.wav"), "E3": play.Sound("notes/E3.wav"),
    "F3": play.Sound("notes/F3.wav"), "G3": play.Sound("notes/G3.wav"), "A3": play.Sound("notes/A3.wav"),
    "B3": play.Sound("notes/B3.wav"),
    "C4": play.Sound("notes/C4.wav"), "D4": play.Sound("notes/D4.wav"), "E4": play.Sound("notes/E4.wav"),
    "F4": play.Sound("notes/F4.wav"), "G4": play.Sound("notes/G4.wav"), "A4": play.Sound("notes/A4.wav"),
    "B4": play.Sound("notes/B4.wav")
}

cap = cv2.VideoCapture(0)
screen_width = int(cap.get(3))
screen_height = int(cap.get(4))

screen_width = screen_width * 2
screen_height = screen_height * 2
cap.set(3, screen_width)
cap.set(4, screen_height)

key_height = screen_height // 3
white_keys = ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4", "B4"]
white_key_width = screen_width // len(white_keys)

active_keys = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    pressed_keys = set()

    for i, key in enumerate(white_keys):
        x_min = i * white_key_width
        x_max = x_min + white_key_width
        y_min = 0  
        y_max = key_height  

        key_color = (255, 200, 200) if key in active_keys else (255, 255, 255)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), key_color, -1)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 0), 2)
        cv2.putText(frame, key, (x_min + 15, y_max - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id in [4, 8, 12, 16, 20]:
                lm = hand_landmarks.landmark[id]
                cx, cy = int(lm.x * screen_width), int(lm.y * screen_height)

                if cy < key_height:
                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                    for i, key in enumerate(white_keys):
                        x_min = i * white_key_width
                        x_max = x_min + white_key_width
                        if x_min <= cx < x_max:
                            pressed_keys.add(key)
                            if key not in active_keys:
                                print(f"Playing {key}")
                                notes[key].play()
                            break

    for key in active_keys - pressed_keys:
        notes[key].stop()

    active_keys = pressed_keys

    cv2.imshow("Pyano", frame)

    if cv2.waitKey(1) == 13 or cv2.getWindowProperty('Pyano', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
