# routes.py
from flask import Flask, Response, request, render_template
from models.gun_detector import GunDetector
from models.image_saver import ImageSaver
from controllers.video_controller import VideoController
from datetime import datetime
import os

app = Flask(__name__)

# Initialize our model components.
gun_detector = GunDetector(
    model_path="yolo11x.pt",
    gun_class_ids=[42, 43, 76],  # Adjust these to match your target classes.
    conf_threshold=0.55,
    gun_map={42: "Garfo", 43: "Knife", 76: "Tesoura"}
)
image_saver_webcam = ImageSaver(base_folder="images/detections/webcam")
image_saver_video = ImageSaver(base_folder="images/detections/videos")

# Create the video controller using the webcam (0)
video_controller = VideoController(0, gun_detector, image_saver_webcam, save_interval=5)

@app.route('/video_feed')
def video_feed():
    """
    Streams the webcam feed with detection overlays.
    """
    return Response(video_controller.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    """
    Allows users to upload a video file for analysis.
    """
    if request.method == 'POST':
        file = request.files.get('video')
        if file:
            now = datetime.now()
            date_str = now.strftime("%Y_%m_%d-%H_%M_%S")
            file_name = file.filename
            folder_path = "uploads/videos/" + date_str
            file_path = folder_path + "/" + file_name

            # Create the directory if it does not exist
            os.makedirs(folder_path, exist_ok=True)

            file.save(file_path)
            # Create a new controller for the uploaded video.
            upload_controller = VideoController(file_path, gun_detector, image_saver_video, save_interval=1)
            return Response(upload_controller.generate_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('upload.html')

@app.route('/')
def index():
    """
    Home page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
