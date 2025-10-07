import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math

# --- 1. Initialization ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()
frame_w, frame_h = 640, 480
cap.set(3, frame_w)
cap.set(4, frame_h)

smoothening = 7  # Adjust for smoother/faster cursor movement
pX, pY = 0, 0  # Previous X and Y positions
cX, cY = 0, 0  # Current X and Y positions

# Define threshold for a 'click' gesture (distance between thumb and index tip)
CLICK_THRESHOLD = 40  # Adjust based on testing

# --- Finger Tip Landmarks (for reference) ---
# TIP_IDs = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky

# --- 2. Frame Processing Loop ---
while True:
    success, frame = cap.read()
    if not success:
        continue

    # Flip the frame for a mirror view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # --- 3. Hand Detection & Tracking ---
    results = hands.process(framergb)

    # --- 4. Landmark Extraction ---
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Get landmarks for Index Finger Tip (8) and Thumb Tip (4)
            # Coordinates are normalized (0 to 1)
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Convert normalized coordinates to pixel values
            x8 = int(index_tip.x * frame_w)
            y8 = int(index_tip.y * frame_h)
            x4 = int(thumb_tip.x * frame_w)
            y4 = int(thumb_tip.y * frame_h)

            # Draw a circle on the index finger tip for visibility
            cv2.circle(frame, (x8, y8), 10, (255, 0, 255), cv2.FILLED)

            # --- 5. Coordinate Mapping (Movement) ---
            # Map hand position to screen resolution
            # Add a padding area (e.g., 100 pixels) to avoid edge jitter

            # Screen coordinates
            X_map = np.interp(x8, (100, frame_w - 100), (0, screen_w))
            Y_map = np.interp(y8, (100, frame_h - 100), (0, screen_h))

            # Smoothen the movement
            cX = pX + (X_map - pX) / smoothening
            cY = pY + (Y_map - pY) / smoothening

            # Move the mouse
            pyautogui.moveTo(cX, cY)
            pX, pY = cX, cY  # Update previous positions

            # --- 6. Gesture Recognition & Action (Clicking) ---

            # Calculate distance between index tip and thumb tip
            dist = math.hypot(x8 - x4, y8 - y4)

            if dist < CLICK_THRESHOLD:
                # Pinch gesture for left click
                cv2.circle(frame, (x8, y8), 10, (0, 255, 0), cv2.FILLED)  # Green circle on click
                pyautogui.click()

            # Draw all landmarks (optional)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # --- 7. Display & Exit ---
    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 8. Cleanup ---
cap.release()
cv2.destroyAllWindows()