import cv2
import mediapipe as mp
import socket
import json

# Updated MediaPipe API
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
unity_address = ("127.0.0.1", 5052)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        landmarks = []
        for lm in results.multi_hand_landmarks[0].landmark:
            landmarks.append({"x": lm.x, "y": lm.y, "z": lm.z})
        
        # Draw landmarks on screen
        mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0], 
                               mp.solutions.hands.HAND_CONNECTIONS)
        
        sock.sendto(json.dumps(landmarks).encode(), unity_address)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
