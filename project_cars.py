import cv2
import mediapipe as mp
import vgamepad as vg

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

gamepad = vg.VX360Gamepad()

def calculate_slope(hand_landmarks):
    if len(hand_landmarks) < 2:
        return None
    x1, y1 = hand_landmarks[0][10].x, hand_landmarks[0][10].y
    x2, y2 = hand_landmarks[1][10].x, hand_landmarks[1][10].y
    slope = ((y2 - y1) / (x2 - x1))*0.9 if x2 != x1 else float('inf')
    return slope

def calculate_distance(hand_landmarks):
    if len(hand_landmarks) < 2:
        return None
    x1, y1 = hand_landmarks[0][10].x, hand_landmarks[0][10].y
    x2, y2 = hand_landmarks[1][10].x, hand_landmarks[1][10].y
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return distance

def control_car(slope, distance):
    if slope is None or distance is None:
        return None
    left_trigger = min(max((distance - 0.5) * 1.3, 0), 1) 
    right_trigger = min(max((0.4 - distance) * 1.3, 0), 1) 
    left_joystick_x = min(max(-(slope), -1), 1) 

    if left_trigger > 0:
        right_trigger = 0
    if right_trigger > 0:
        left_trigger = 0

    if(left_joystick_x == -1 or left_joystick_x == 1):
        left_trigger = left_trigger/3
        right_trigger = right_trigger/3
        
    print(left_joystick_x)

    
    gamepad.left_joystick_float(x_value_float=left_joystick_x, y_value_float=0)
    

    if right_trigger > 0:
        gamepad.left_trigger_float(0)
        status = 'Decelerating'
        gamepad.right_trigger_float(right_trigger)
        


    elif left_trigger > 0:
        gamepad.right_trigger_float(0)
        gamepad.left_trigger_float(left_trigger)
        status = 'Accelerating'
        
    
    else:
        gamepad.right_trigger_float(0)
        gamepad.left_trigger_float(0)
        status = 'Stable'

    gamepad.update()

    return status

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    status = 'No hands detected'
    if results.multi_hand_landmarks:
        hand_landmarks = []
        for hand_landmark in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
            hand_landmarks.append(hand_landmark.landmark)
        if len(hand_landmarks) >= 2:
            slope = calculate_slope(hand_landmarks)
            distance = calculate_distance(hand_landmarks)
            status = control_car(slope, distance)
    
    color = (0, 255, 0)
    if status == 'Accelerating':
        color = (0, 0, 255) 
    elif status == 'Decelerating':
        color = (255, 0, 0) 
    
    cv2.putText(frame, f'Status: {status}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    cv2.imshow('Hand Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
