import cv2
import sys
from lines import estimate_distance_from_screen
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
should_process_video = False
face_data = {}
CORS(app)  # Enable CORS for all routes

@app.route('/send_face_data', methods=['POST'])
def send_face_data():
    global face_data
    data = request.json
    face_data = data

@app.route('/get_face_data', methods=['GET'])
def get_face_data():
    global face_data
    return face_data

@app.route('/start_processing', methods=['POST'])
def start_processing():
    global should_process_video
    should_process_video = True
    capture_video()

@app.route('/stop_processing', methods=['POST'])
def stop_processing():
    global should_process_video
    should_process_video = False

def capture_video():
    global should_process_video

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    video_capture = cv2.VideoCapture(0) # video source

    while should_process_video:
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
            face_midpoint_data = {
                "x": int(face_midpoint[0]),
                "y": int(face_midpoint[1]),
            }
            url = "http://127.0.0.1:5001/send_face_data"
            requests.post(url, json=jsonify(face_midpoint_data))
            
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
