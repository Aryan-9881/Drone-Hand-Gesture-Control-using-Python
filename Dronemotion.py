import cv2
import mediapipe as mp
import pybullet as p
import pybullet_data
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Connect to PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the drone URDF
drone = p.loadURDF("E:/PRACTICE/URDF_Files/quadrotor.urdf", [0, 0, 1])

# Open the default camera
cap = cv2.VideoCapture(0)

# Initialize variables for previous thumb and palm positions
prev_thumb_y = 0
prev_palm_y = 0
prev_palm_x = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image)

    # Draw the hand annotations on the image
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the positions of specific landmarks
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            palm = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Calculate thumb movement direction (up or down)
            if thumb_tip.y < prev_thumb_y:  # Thumbs-up gesture (thumb higher than previous position)
                # Move drone upwards
                current_position = p.getBasePositionAndOrientation(drone)[0]
                new_position = [current_position[0], current_position[1], current_position[2] + 0.1]  # Adjust the increment as needed
                p.resetBasePositionAndOrientation(drone, new_position, [0, 0, 0, 1])  # Update drone position in AR/VR
                print("Moving drone upwards")

            elif thumb_tip.y > prev_thumb_y:  # Thumbs-down gesture (thumb lower than previous position)
                # Move drone downwards
                current_position = p.getBasePositionAndOrientation(drone)[0]
                new_position = [current_position[0], current_position[1], current_position[2] - 0.1]  # Adjust the decrement as needed
                p.resetBasePositionAndOrientation(drone, new_position, [0, 0, 0, 1])  # Update drone position in AR/VR
                print("Moving drone downwards")

            # Update previous thumb position
            prev_thumb_y = thumb_tip.y

            # Calculate palm movement direction (up or down)
            if palm.y < prev_palm_y:  # Palm moved upwards
                # Move drone upwards
                current_position = p.getBasePositionAndOrientation(drone)[0]
                new_position = [current_position[0], current_position[1], current_position[2] + 0.1]  # Adjust the increment as needed
                p.resetBasePositionAndOrientation(drone, new_position, [0, 0, 0, 1])  # Update drone position in AR/VR
                print("Moving drone upwards based on palm movement")

            elif palm.y > prev_palm_y:  # Palm moved downwards
                # Move drone downwards
                current_position = p.getBasePositionAndOrientation(drone)[0]
                new_position = [current_position[0], current_position[1], current_position[2] - 0.1]  # Adjust the decrement as needed
                p.resetBasePositionAndOrientation(drone, new_position, [0, 0, 0, 1])  # Update drone position in AR/VR
                print("Moving drone downwards based on palm movement")

            # Calculate palm movement direction (left or right)
            if palm.x < prev_palm_x:  # Palm moved left
                # Move drone left
                current_position = p.getBasePositionAndOrientation(drone)[0]
                new_position = [current_position[0] - 0.1, current_position[1], current_position[2]]  # Adjust the decrement as needed
                p.resetBasePositionAndOrientation(drone, new_position, [0, 0, 0, 1])  # Update drone position in AR/VR
                print("Moving drone left based on palm movement")

            elif palm.x > prev_palm_x:  # Palm moved right
                # Move drone right
                current_position = p.getBasePositionAndOrientation(drone)[0]
                new_position = [current_position[0] + 0.1, current_position[1], current_position[2]]  # Adjust the increment as needed
                p.resetBasePositionAndOrientation(drone, new_position, [0, 0, 0, 1])  # Update drone position in AR/VR
                print("Moving drone right based on palm movement")

            # Update previous palm positions
            prev_palm_y = palm.y
            prev_palm_x = palm.x

    # Display the image
    cv2.imshow('AR/VR Controlled Drone', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
