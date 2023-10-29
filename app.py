import cv2
import sys
from lines import estimate_distance_from_screen
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

video_capture = cv2.VideoCapture(0) # video source

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=15,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    height, width, channels = frame.shape
    center_coordinates = (width // 2, height // 2)

    green_color = (0, 255, 0)
    pink_color = (255, 0 , 255)
    border_thickness = 2
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), green_color, border_thickness)
        
        dist = estimate_distance_from_screen((x,y,w,h))

        # display_text = f"{w} x {h} = {w*h}\n {dist}"
        face_midpoint = (x + w // 2,  y + h // 2)

        #-1 * abs(Face midpoint - center) + midpoint 

        projected_pointx = -1 * (face_midpoint[0] - center_coordinates[0]) + center_coordinates[0]
        projected_pointy = -1 * (face_midpoint[1] - center_coordinates[1]) + center_coordinates[1]

        display_text = f"{projected_pointx, projected_pointy} {face_midpoint} {center_coordinates}"

        cv2.putText(frame, display_text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        cv2.arrowedLine(frame, center_coordinates,(projected_pointx, projected_pointy), pink_color, border_thickness)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('p'):
        print(faces[0])

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()