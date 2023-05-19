import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify a different index if you have multiple cameras

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame in a window
    cv2.imshow('Camera', frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
