# routes.py
from flask import Flask, Response, request, render_template, redirect, url_for
from models.gun_detector import GunDetector
#from models.custom_detector import CustomDetector  # If implemented
from models.image_saver import ImageSaver
from controllers.video_controller import VideoController
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates')

def get_detector(model_name):
    """
    Returns a detector instance based on the provided model name.
    """
    if model_name == 'custom':
        return GunDetector(
            model_path="best_5.pt",
            gun_class_ids=[0,1,2,3],
            conf_threshold=0.55,
            gun_map={0: "Faca", 1: "Tesoura", 2: "Pistola", 3: "Pistola"}
        )
    else:
        return GunDetector(
            model_path="yolo11x.pt",
            gun_class_ids=[42, 43, 76],
            conf_threshold=0.25,
            gun_map={42: "Garfo", 43: "Faca", 76: "Tesoura"}
        )

# Separate image saver instances for webcam and video.
image_saver_webcam = ImageSaver(base_folder="images/detections/webcam")
image_saver_video = ImageSaver(base_folder="images/detections/videos")

@app.route('/')
def index():
    # Render the index.html template.
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    model_name = request.args.get('model', 'yolo')
    print(f"Using model We: {model_name}")
    detector = get_detector(model_name)
    video_controller = VideoController(0, detector, image_saver_webcam, save_interval=5)
    return Response(video_controller.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/view_feed')
def view_feed():
    model_name = request.args.get('model')
    print(f"Using model View: {model_name}")
    return render_template('video_view.html',  model=model_name)

# Rota para processar o upload de vídeo.
@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        file = request.files.get('video')
        model_name = request.form.get('model').lower()
        print(f"Using model: {model_name}")
        if file:
            now = datetime.now()
            date_str = now.strftime("%Y_%m_%d-%H_%M_%S")
            file_name = file.filename
            folder_path = os.path.join("uploads", "videos", date_str)
            file_path = os.path.join(folder_path, file_name)
            os.makedirs(folder_path, exist_ok=True)
            file.save(file_path)
            # Após salvar o vídeo, redireciona para a página de visualização do vídeo.
            return redirect(url_for('view_video_upload', model=model_name, file=file_path))
    model_name = request.args.get('model')
    return render_template('upload.html', model=model_name)

# Rota que renderiza o template com o layout para análise de vídeo.
@app.route('/view_video_upload')
def view_video_upload():
    model_name = request.args.get('model', 'yolo').lower()
    file_path = request.args.get('file')
    return render_template('video_upload_view.html', model=model_name, file=file_path)

# Rota que fornece o feed de vídeo processado para o vídeo enviado.
@app.route('/video_upload_feed')
def video_upload_feed():
    model_name = request.args.get('model', 'yolo').lower()
    file_path = request.args.get('file')
    print(f"Using model (upload): {model_name} para arquivo {file_path}")
    detector = get_detector(model_name)
    video_controller = VideoController(file_path, detector, image_saver_video, save_interval=1)
    return Response(video_controller.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
