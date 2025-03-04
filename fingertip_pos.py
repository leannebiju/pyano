import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            for id, lm in enumerate(hand_landmarks.landmark): #id gives the landmark and lm the x,y,z coordinates
                h, w, _ = frame.shape #width and height of the frame
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert normalized values to pixel positions by multiplying with the width and height

                if id in [4, 8, 12, 16, 20]:  # Fingertips
                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Draw a green dot
                    #print(f"Fingertip {id}: X={cx}, Y={cy}")

    frame = cv2.flip(frame, 1) 
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) == 13 or cv2.getWindowProperty('Hand Tracking', cv2.WND_PROP_VISIBLE) == 0:
        break

cap.release()
cv2.destroyAllWindows()
