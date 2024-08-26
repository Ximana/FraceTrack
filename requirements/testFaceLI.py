

import face_recognition
from PIL import Image
import numpy as np

image_path = "app/static/img/pessoasDesaparecidas/testeIMG/A/24630_7E9A5B3C65889D88.jpg"

image = Image.open(image_path)
image = image.convert('RGB')
rgb_image = np.array(image)
print(f"Image shape: {rgb_image.shape}")
print(f"Image dtype: {rgb_image.dtype}")

face_encodings = face_recognition.face_encodings(rgb_image)
print(f"Number of faces found: {len(face_encodings)}")
