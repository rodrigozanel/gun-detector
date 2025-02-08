# controllers/video_controller.py
import time
import cv2

class VideoController:
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
        success, frame = self.cap.read()
        if not success:
            return None, None

        processed_frame, detections = self.detector.analyze_frame(frame)

        # If detections exist and we haven't saved recently, save the frame.
        if detections:
            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                # You might choose which detection to use. Here, we use the first.
                label = detections[0]['label']
                self.image_saver.save_image(frame, label)
                self.last_save_time = current_time

        return processed_frame, detections

    def generate_frames(self):
        """
        Generator that yields JPEG-encoded frames.
        """
        while True:
            processed_frame, _ = self.process_frame()
            if processed_frame is None:
                break
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
