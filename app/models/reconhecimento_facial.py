import face_recognition
import os
import cv2
import numpy as np
import pickle
from datetime import datetime
from app import db
from app.models.detecao import Deteccao

class ReconhecimentoFacial:
    def __init__(self):
        self.model_path = 'app/ml/facial_recognition_model.pkl'
        self.known_face_encodings = []
        self.known_face_names = []

    def treinar_modelo(self, imagem_diretorio):
        """
        Treina o modelo de reconhecimento facial com as imagens do diretório fornecido.
        """
        self.known_face_encodings = []
        self.known_face_names = []

        for imagem_nome in os.listdir(imagem_diretorio):
            if imagem_nome.endswith(('png', 'jpg', 'jpeg')):
                caminho_imagem = os.path.join(imagem_diretorio, imagem_nome)
                imagem = face_recognition.load_image_file(caminho_imagem)
                face_encodings = face_recognition.face_encodings(imagem)

                if face_encodings:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(imagem_nome.split('.')[0])

        # Serializar os encodings e nomes das faces conhecidas
        with open(self.model_path, 'wb') as model_file:
            pickle.dump({
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }, model_file)

    def reconhecer(self, frame):
        """
        Reconhece as faces no frame fornecido e salva a imagem capturada e as detecções na base de dados.
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("O modelo de reconhecimento facial não foi encontrado. Treine o modelo primeiro.")

        with open(self.model_path, 'rb') as model_file:
            data = pickle.load(model_file)
            self.known_face_encodings = data['encodings']
            self.known_face_names = data['names']

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Desconhecido"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)

            # Salvar a imagem capturada
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            captured_image_path = os.path.join('app/static/img/pessoasDetetadas', f'{name}_{timestamp}.jpg')
            cv2.imwrite(captured_image_path, frame)

            # Salvar a detecção na base de dados
            deteccao = Deteccao(
                pessoa_id=best_match_index,  # ou use um mapeamento apropriado para a pessoa_id
                localizacao='Local não especificado',
                imagem_capturada=captured_image_path
            )
            db.session.add(deteccao)
            db.session.commit()

        return frame
