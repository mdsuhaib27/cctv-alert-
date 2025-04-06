import os
import requests
from ultralytics import YOLO
import cv2

# Model path
MODEL_PATH = r"s:\Mohamed Suhaib\Downloads\best.pt\Weapons-and-Knives-Detector-with-YOLOv8-main\runs\detect\Haar_Compressed\weights\best.pt"



MODEL_URL = "https://github.com/mohamed-suhaib-ai/Weapons-and-Knives-Detector-with-YOLOv8/releases/download/model/best.pt"

# Auto-download model if not found
if not os.path.exists(MODEL_PATH):
    print("[INFO] Model not found locally. Downloading...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)
    print("[INFO] Model downloaded successfully.")

# Load YOLO model
yolo_model = YOLO(MODEL_PATH)

# Detection function
def detect_objects(frame):
    results = yolo_model(frame)[0]
    detections = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = yolo_model.names[cls_id]
        if conf > 0.5:
            detections.append((label, conf))
            # Draw box
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 0, 255), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (xyxy[0], xyxy[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return detections
