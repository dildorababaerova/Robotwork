import cv2
import numpy as np
import time
import pygame  # For playing sound in Linux

# Initialize the camera
cap = None  # Camera is initially off
camera_enabled = False  # Flag to track camera state

# Function to toggle the camera on/off
def toggle_camera():
    global cap, camera_enabled
    if camera_enabled:
        # If the camera is on, turn it off
        if cap is not None:
            cap.release()
            cv2.destroyAllWindows()
            print("Camera turned off.")
        camera_enabled = False
    else:
        # If the camera is off, turn it on
        cap = cv2.VideoCapture(0)  # Use the default camera
        if not cap.isOpened():
            print("Error opening the camera!")
            return
        print("Camera turned on.")
        camera_enabled = True

# Function to check available cameras
def check_cameras():
    # Try to open multiple cameras by index
    for i in range(2):  # Check up to 2 cameras (can be increased)
        temp_cap = cv2.VideoCapture(i)
        if temp_cap.isOpened():
            print(f"Camera {i} is available.")
            temp_cap.release()
        else:
            print(f"Camera {i} is not available.")

check_cameras()

# Function to load a new graphic (e.g., an image)
def load_new_graphic(image_path):
    return cv2.imread(image_path)

# Paths to images (graphics)
image_paths = ['graphic1.jpg']  # List of image paths
image_index = 0  # Index for switching between images

# Load the first image
graphic = load_new_graphic(image_paths[image_index])

# Time for updating the graphic (50 seconds)
last_update_time = time.time()  # Timestamp of the last update

# Initialize pygame for playing sound
pygame.mixer.init()

# Function to signal a change in the graphic
def signal_change():
    print("Graphic change detected! Alarm activated.")
    
    # Play a sound signal
    pygame.mixer.music.load("beep.wav")  # Load the sound file
    pygame.mixer.music.play()  # Play the sound

    # Display a warning on the screen
    cv2.putText(frame, "CHANGE DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Main program loop
while True:
    # If the camera is enabled, process frames
    if camera_enabled:
        ret, frame = cap.read()  # Capture a frame from the camera
        if not ret:
            print("Failed to capture image from the camera!")
            break

        # Convert the current camera frame to grayscale for comparison
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert the graphic to grayscale for comparison
        gray_graphic = cv2.cvtColor(graphic, cv2.COLOR_BGR2GRAY)

        # Resize the graphic if it doesn't match the frame size
        if gray_graphic.shape != gray_frame.shape:
            gray_graphic = cv2.resize(gray_graphic, (gray_frame.shape[1], gray_frame.shape[0]))

        # Compare frames (detect changes)
        diff = cv2.absdiff(gray_frame, gray_graphic)
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        changes = np.count_nonzero(thresh)

        # If changes exceed the threshold, draw a rectangle and trigger the alarm
        if changes > 1000:
            cv2.rectangle(frame, (50, 50), (200, 200), (0, 255, 0), 2)
            signal_change()  # Trigger the alarm
        
        # Display the current camera frame
        cv2.imshow('Frame', frame)

        # Check the time for updating the graphic
        current_time = time.time()
        if current_time - last_update_time > 0.50:  # 0.50 seconds
            # Update the graphic if 50 seconds have passed
            image_index = (image_index + 1) % len(image_paths)  # Switch to the next image
            graphic = load_new_graphic(image_paths[image_index])  # Load a new image
            last_update_time = current_time  # Update the last update time

    # Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Exit the program
        break
    elif key == ord('c'):  # Toggle the camera on/off
        toggle_camera()

# Release resources
if cap is not None:
    cap.release()
cv2.destroyAllWindows()