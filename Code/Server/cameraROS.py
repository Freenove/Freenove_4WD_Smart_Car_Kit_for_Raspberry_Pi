import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco

# ROS initialization
rospy.init_node('camera_node')
bridge = CvBridge()

# Load the pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-defined dictionary for ArUco codes
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)

# Create the ArUco parameters
parameters = aruco.DetectorParameters_create()

# Callback function to process the camera image
def process_image(msg):
    # Convert ROS Image message to OpenCV image
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Detect ArUco markers in the grayscale frame
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Draw detected ArUco markers and their IDs
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i in range(len(ids)):
            cv2.putText(frame, str(ids[i][0]), (corners[i][0][0][0], corners[i][0][0][1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Camera', frame)
    cv2.waitKey(1)

# Subscribe to the camera topic
rospy.Subscriber('/camera_topic', Image, process_image)

# Spin ROS
rospy.spin()

# Close OpenCV windows
cv2.destroyAllWindows()

