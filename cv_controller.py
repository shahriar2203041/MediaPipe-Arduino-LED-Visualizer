import cv2
import mediapipe as mp
import serial
import time

# Ensure this COM port is correct for your Arduino
PORT_NAME = 'COM5' 

try:
    arduino = serial.Serial(port=PORT_NAME, baudrate=9600, timeout=0.1)
    print(f"Successfully connected to Arduino on {PORT_NAME}")
    time.sleep(2)
except serial.SerialException as e:
    print(f"FATAL ERROR: Could not connect to Arduino on {PORT_NAME}.")
    exit()

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]

# Webcam setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
last_sent_count = -1

print("\nStarting camera... Show 1-4 fingers. Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        continue
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    total_finger_count = 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            fingers_on_this_hand = []
            if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
                fingers_on_this_hand.append(1)
            else:
                fingers_on_this_hand.append(0)

            for id in range(1, 5):
                if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                    fingers_on_this_hand.append(1)
                else:
                    fingers_on_this_hand.append(0)
            
            total_finger_count += fingers_on_this_hand.count(1)

    # Send the finger count to Arduino if it has changed
    if total_finger_count != last_sent_count:
        arduino.write(str(total_finger_count).encode())
        print(f"Sent finger count: {total_finger_count}")
        last_sent_count = total_finger_count

    cv2.putText(img, f"Sending: {total_finger_count}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("CV LED Bar Graph", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
print("Closing program.")
arduino.close()
cap.release()
cv2.destroyAllWindows()
