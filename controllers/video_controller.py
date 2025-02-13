# controllers/video_controller.py
import time
import cv2
#from skimage.metrics import structural_similarity as ssim
# import structural_similarity from scikit-image
import numpy as np
from domain.NotificationDTO import NotificationDTO
import os
from dotenv import load_dotenv
from services.NotificationService import NotificationService
import os


def mse(imageA, imageB):
    # Compute the Mean Squared Error between two images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def is_similar(frame1, frame2, threshold):
    """Compara dois frames usando SSIM para detectar mudanças."""
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    #score, _ = ssim(gray1, gray2, full=True)
    score = mse(gray1, gray2)
    return score > threshold


class VideoController:
    similarity_threshold = 0.50
    last_processed_frame = None
    notification_service = NotificationService()
    # create a colletion of detections so we can dispatch them to the notification service each 5 images or 30 seconds
    detectionsToNotify = []
    initialTime = time.time()

    notification_interval = int(os.getenv("NOTIFICATIONS_INTERVAL", 30))
    notifications_enabled = os.getenv("NOTIFICATIONS_ENABLED", True)
    notifications_bucket_size = int(os.getenv("NOTIFICATIONS_BUCKET_SIZE", 5))

    """
    Handles the video stream: reading frames, passing them to the detector,
    and saving images when a detection is made (with a configurable save interval).
    """
    def __init__(self, video_source, detector, image_saver, save_interval=1):
        """
        :param video_source: 0 for webcam or a file path.
        :param detector: An instance of GunDetector.
        :param image_saver: An instance of ImageSaver.
        :param save_interval: Minimum seconds between saved frames.
        """
        self.video_source = video_source
        self.detector = detector
        self.image_saver = image_saver
        self.cap = cv2.VideoCapture(video_source)
        self.save_interval = save_interval
        self.last_save_time = 0

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def process_frame(self):

        # Check if it's time to send the notifications
        passedTime = round(time.time() - self.initialTime, 0)
        print(f"Next notification in {self.notification_interval - passedTime} seconds or when {self.notifications_bucket_size} detections are collected (currently {len(self.detectionsToNotify)}).")
        if (passedTime >= self.notification_interval and len(self.detectionsToNotify) >= 0) or len(self.detectionsToNotify) >= self.notifications_bucket_size:
            if self.notifications_enabled:
                self.notification_service.send_notification(self.detectionsToNotify)
                self.detectionsToNotify = []
                self.initialTime = time.time()
            else :
                print("Notifications are disabled.")

        file_path = None
        success, frame = self.cap.read()
        if not success:
            return None, None

        processed_frame, detections = self.detector.analyze_frame(frame)

        # If detections exist, and we haven't saved recently, save the frame.
        if detections:            
            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                # You might choose which detection to use. Here, we use the first.
                label = detections[0]['label']
                # Collect the precision of the detection
                precision = detections[0]['confidence']

                # Check if the current frame is similar to the last one.
                _is_similar = self.last_processed_frame is not None and is_similar(self.last_processed_frame, processed_frame, self.similarity_threshold)
                if _is_similar:
                    return processed_frame, detections

                self.last_processed_frame = processed_frame
                file_path = self.image_saver.save_image(frame, label)
                self.last_save_time = current_time
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                #print(f"Precisão: {precision}")
                notification = NotificationDTO(label, file_path, current_time, precision)
                self.detectionsToNotify.append(notification)
        else:
            self.last_processed_frame = None

        return processed_frame, detections

    def generate_frames(self):
        """
        Generator that yields JPEG-encoded frames.
        """
        _is_similar = False
        _process_started = False
        
        while True:
            processed_frame, _ = self.process_frame()
            if processed_frame is None:
                # força o envio da notificação porque o video acabou
                self.notification_service.send_notification(self.detectionsToNotify)
                _process_started = False
                break
            else:
                _process_started = True

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
