import os
import face_recognition
import pickle
from typing import List, Tuple
import cv2
import numpy as np
from datetime import datetime
from app import db
from app.models.detecao import Deteccao
from app.models.pessoa_desaparecida import PessoaDesaparecida

class ReconhecimentoFacial:
    def __init__(self):
        self.known_face_encodings: List[List[float]] = []
        self.known_face_names: List[str] = []
        self.load_model()

    def load_model(self):
        model_path = "app/static/ml/facial_recognition_model.pkl"
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)
        else:
            print("Modelo não encontrado. Execute treinar_modelo() primeiro.")

    def process_image(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Failed to read image: {img_path}")
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
                        print(f"Processado: {filename}")
                    else:
                        print(f"Sem rosto emcontrado {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

        model_data: Tuple[List[List[float]], List[str]] = (self.known_face_encodings, self.known_face_names)
        with open(os.path.join(ml_dir, "facial_recognition_model.pkl"), "wb") as f:
            pickle.dump(model_data, f)

        print(f"Model trained with {len(self.known_face_names)} faces and saved to {ml_dir}")

    def reconhecer(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Desconhecido"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]

                img_nome = name + ".jpg"
                print(f"O nome e: {img_nome}")

                # Salvar a imagem
                img_path = self.save_detected_image(frame, name)

                # Salvar o registro na base de dados
                self.save_detection(name, img_path)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

    def save_detected_image(self, frame, name):
        output_dir = "app/static/img/pessoasDetetadas/"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.jpg"
        img_path = os.path.join(output_dir, filename)
        cv2.imwrite(img_path, frame)
        return img_path

    def save_detection(self, name, img_path):
        pessoa = PessoaDesaparecida.query.filter_by(imagem=name).first()
        if pessoa:
            detecao = Deteccao(
                pessoa_id=pessoa.id,
                imagem_capturada=os.path.relpath(img_path, "app/static"),
                localizacao="Câmera local"  # Você pode ajustar isso conforme necessário
            )
            db.session.add(detecao)
            db.session.commit()
        else:
            print(f"Pessoa não encontrada no banco de dados: {name}")