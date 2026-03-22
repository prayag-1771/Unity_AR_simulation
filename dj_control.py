import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

last_action_time = 0
cooldown = 1.0

def get_finger_states(landmarks):
    # Returns [thumb, index, middle, ring, pinky] - 1=up, 0=down
    fingers = []
    fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if landmarks[tip].y < landmarks[tip-2].y else 0)
    return fingers

def detect_gesture(fingers, landmarks):
    thumb, index, middle, ring, pinky = fingers

    if all(f == 1 for f in fingers):
        return "PLAY_PAUSE"
    if all(f == 0 for f in fingers):
        return "SHUFFLE"
    if index == 1 and middle == 0 and ring == 0 and pinky == 0:
        if landmarks[8].x > landmarks[0].x + 0.3:
            return "NEXT"
        elif landmarks[8].x < landmarks[0].x - 0.3:
            return "PREV"
    if index == 1 and middle == 1 and ring == 0 and pinky == 0:
        return "VOL_UP" if landmarks[9].y < 0.4 else "VOL_DOWN"
    if pinky == 1 and index == 0 and middle == 0 and ring == 0:
        return "EQ_RIGHT" if landmarks[20].x > 0.6 else "EQ_LEFT"
    return None

def perform_action(gesture):
    actions = {
        "PLAY_PAUSE": Key.media_play_pause,
        "NEXT":       Key.media_next,
        "PREV":       Key.media_previous,
        "VOL_UP":     Key.media_volume_up,
        "VOL_DOWN":   Key.media_volume_down,
    }
    if gesture in actions:
        keyboard.press(actions[gesture])
        keyboard.release(actions[gesture])
    elif gesture == "SHUFFLE":
        keyboard.press('s')
        keyboard.release('s')
    elif gesture == "EQ_RIGHT":
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif gesture == "EQ_LEFT":
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    print(gesture)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        fingers = get_finger_states(hand.landmark)
        gesture = detect_gesture(fingers, hand.landmark)

        if gesture:
            cv2.putText(frame, gesture, (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        current_time = time.time()
        if gesture and (current_time - last_action_time) > cooldown:
            perform_action(gesture)
            last_action_time = current_time

    cv2.imshow("DJ Hand Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
