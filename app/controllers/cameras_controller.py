# app/controllers/cameras_controller.py

from flask import Blueprint, render_template, Response
import cv2
import logging

cameras_bp = Blueprint('cameras', __name__, url_prefix='/cameras')

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Erro ao abrir a camera")
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            logger.error("Erro ao ler o frame")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@cameras_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@cameras_bp.route('/webcam')
def webcam():
    return render_template('cameras/webcam.html')

@cameras_bp.route('/stop_camera')
def stop_camera():
    return "Camera parada"
