import cv2
import mediapipe as mp
import pygame.mixer as play

# Initialize MediaPipe and Pygame
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

play.init()
notes = {
    "C": play.Sound("sounds/c1.wav"),
    "D": play.Sound("sounds/d1.wav"),
    "E": play.Sound("sounds/e1.wav"),
    "F": play.Sound("sounds/f1.wav"),
    "G": play.Sound("sounds/g1.wav"),
    "A": play.Sound("sounds/a1.wav"),
    "B": play.Sound("sounds/b1.wav")
}

cap = cv2.VideoCapture(0)
screen_width = int(cap.get(3))  
screen_height = int(cap.get(4))

# Define white key positions (7 keys)
white_keys = ["C", "D", "E", "F", "G", "A", "B"]
white_key_width = screen_width // 7
white_key_height = screen_height // 2  # Only in top half

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    # Draw white keys
    for i, key in enumerate(white_keys):
        x_min = i * white_key_width
        x_max = x_min + white_key_width
        cv2.rectangle(frame, (x_min, 0), (x_max, white_key_height), (255, 255, 255), -1)  # White key
        cv2.rectangle(frame, (x_min, 0), (x_max, white_key_height), (0, 0, 0), 2)  # Black border
        cv2.putText(frame, key, (x_min + 20, white_key_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 0), 2, cv2.LINE_AA)  # Label

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            for id in [4, 8, 12, 16, 20]:  # Fingertip landmarks
                lm = hand_landmarks.landmark[id]
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  

                # Check if the fingertip is in the top half (where the keys are)
                if cy < white_key_height:
                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Mark fingertip
                    
                    # Detect which white key is pressed
                    for i, key in enumerate(white_keys):
                        x_min = i * white_key_width
                        x_max = x_min + white_key_width
                        if x_min <= cx < x_max:
                            print(f"Playing {key}")
                            notes[key].play()  # Play the detected note
                            break

    cv2.imshow("Virtual Piano", frame)

    if cv2.waitKey(1) == 13 or cv2.getWindowProperty('Virtual Piano', cv2.WND_PROP_VISIBLE) == 0:
        break

cap.release()
cv2.destroyAllWindows()
