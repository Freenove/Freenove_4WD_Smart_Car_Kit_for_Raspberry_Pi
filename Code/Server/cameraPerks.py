import cv2
import cv2.aruco as aruco

# Load the pre-defined dictionary for ArUco codes
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)

# Create the ArUco parameters
parameters = aruco.DetectorParameters_create()

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify a different index if you have multiple cameras

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the grayscale frame
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Draw detected ArUco markers and their IDs
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i in range(len(ids)):
            cv2.putText(frame, str(ids[i][0]), (corners[i][0][0][0], corners[i][0][0][1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame in a window
    cv2.imshow('Camera', frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()