from flask import Flask, render_template, Response, request, redirect
import cv2
import threading
import os
from face_recognition import recognize_faces
from object_detection import detect_objects
from behavior_analysis import detect_behavior
from alert_system import send_alert

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

camera = None
known_faces = {
    'John': 'john.jpg',
    'Jane': 'jane.jpg'
}

def async_send_alert(subject, message, frame):
    thread = threading.Thread(target=send_alert, args=(subject, message, frame))
    thread.start()

def gen_frames():
    global camera
    while camera and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break

        # Face Recognition
        faces = recognize_faces(frame, known_faces)

        # Object Detection
        detections = detect_objects(frame)

        # Behavior Analysis
        status = detect_behavior([cls for cls, _ in detections])

        # Alerts
        if faces:
            for person in faces:
                async_send_alert("Face Match Alert", f"Detected: {person}", frame)

        if status == "threat":
            async_send_alert("Threat Alert", "Dangerous object or behavior detected!", frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera
    camera = cv2.VideoCapture(0)  # Start webcam
    return redirect('/')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    global camera
    video = request.files['video']
    if video:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(video_path)
        camera = cv2.VideoCapture(video_path)
    return redirect('/')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
