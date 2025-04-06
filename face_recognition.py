
from deepface import DeepFace
import cv2
import numpy as np
import os

# Load face database (embeddings will be stored for faster comparison)
def load_face_database(db_path="known_faces"):
    print("[INFO] Building face embeddings...")
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    return db_path  # DeepFace will use this folder directly in `find`

# Recognize faces using DeepFace.find() for speed
def recognize_faces(frame, db_path="known_faces", threshold=0.35):
    results = []
    try:
        temp_path = "temp_frame.jpg"
        cv2.imwrite(temp_path, frame)
        matches = DeepFace.find(
            img_path=temp_path,
            db_path=db_path,
            model_name="VGG-Face",
            enforce_detection=False,
            distance_metric="cosine"
        )
        if len(matches) > 0 and len(matches[0]) > 0:
            for index, row in matches[0].iterrows():
                identity = os.path.basename(row["identity"])
                results.append(identity)
    except Exception as e:
        print(f"[ERROR] Face recognition error: {e}")
    return results
