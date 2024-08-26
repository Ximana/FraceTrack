import os
import face_recognition
import pickle
from typing import List, Tuple
import cv2
import numpy as np

class ReconhecimentoFacial:
    def __init__(self):
        self.known_face_encodings: List[List[float]] = []
        self.known_face_names: List[str] = []

    def process_image(self, img_path: str) -> np.ndarray:
        # Read image with OpenCV
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Failed to read image: {img_path}")

        # Convert BGR to RGB
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rgb_img

    def treinar_modelo(self):
        img_dir = "app/static/img/pessoasDesaparecidas/testeIMG/A"
        ml_dir = "app/static/ml"

        os.makedirs(ml_dir, exist_ok=True)

        for filename in os.listdir(img_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                name = os.path.splitext(filename)[0]
                img_path = os.path.join(img_dir, filename)

                try:
                    img_array = self.process_image(img_path)
                    face_encodings = face_recognition.face_encodings(img_array)

                    if face_encodings:
                        self.known_face_encodings.append(face_encodings[0])
                        self.known_face_names.append(name)
                        print(f"Processed: {filename}")
                    else:
                        print(f"No face found in {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

        model_data: Tuple[List[List[float]], List[str]] = (self.known_face_encodings, self.known_face_names)
        with open(os.path.join(ml_dir, "facial_recognition_model.pkl"), "wb") as f:
            pickle.dump(model_data, f)

        print(f"Model trained with {len(self.known_face_names)} faces and saved to {ml_dir}")

# Usage:
# rf = ReconhecimentoFacial()
# rf.treinar_modelo()
