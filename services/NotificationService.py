import queue
import threading
import time
import os
from dotenv import load_dotenv

from scipy.constants import precision

from repositories.FileRepository import FileRepository
from services.BrevoService import SendinblueService


class NotificationService:
    def __init__(self):
        """Create a queue to store notifications and start a worker thread."""
        self.notification_queue = queue.Queue()
        self._stop_event = threading.Event()  # Event to stop the thread
        self.worker_thread = threading.Thread(target=self.process_notification, daemon=True)
        self.worker_thread.start()  # Start the thread
        self.brevo_service = SendinblueService()
        self.file_repository = FileRepository()
        # https://d2ewtyh765sd5v.cloudfront.net/Tesoura_20250208_201012_580185.jpg
        self.cdn_url = os.getenv("CDN_URL")

    def process_notification(self):
        """Continuously process notifications from the queue."""
        while not self._stop_event.is_set():
            try:
                detections_to_notify = self.notification_queue.get(timeout=1)  # Wait for 1 second
                print(f"Processing notification for {len(detections_to_notify)} detections...")
                # Process the detections (NotificationDTO objects)
                for detection in detections_to_notify:
                    # [label, file_path, current_time
                    print(f"Detected {detection.get_label()} at {detection.get_current_time()}.")
                    print(f"Saved image to {detection.get_file_path()}.")
                    self.file_repository.upload_file(file_name=detection.get_file_path())

                # Send an email with the detections
                if len(detections_to_notify) > 0:
                    print("Sending email notification...")
                    email = 'rodrigozanelsp@gmail.com'
                    subject = 'Alerta de detecção de armas! Fique seguro! [Isto é um teste]'
                    body = self.generate_html_body(detections_to_notify)
                    self.brevo_service.send_email(email, subject, body)
                    print("Email sent successfully!")
                else :
                    print("No detections to notify.")

                self.notification_queue.task_done()
            except queue.Empty:
                continue  # Continue waiting for notifications

    def send_notification(self, detectionsToNotify):
        """Adds a new notification to the queue."""
        # Add the event to the queue
        self.notification_queue.put(detectionsToNotify)

    def stop(self):
        """Stops the notification thread gracefully."""
        self._stop_event.set()  # Stop the thread
        self.worker_thread.join()  # Wait for the thread to finish

    # generate a HTML body for the email including each image as part of the body
    def generate_html_body(self, detections):
        body = "<h1>Alerta de Detecção de Arma</h1>"
        # Add a note informing the user about it's a test
        body += "<p>Este é um e-mail de teste para informá-lo sobre a detecção de uma arma..</p>"
        for detection in detections:
            # extract the file name from the detection object (it's the last part of the path)
            file_path = detection.get_file_path()
            file_name = os.path.basename(file_path)
            file_url = f"{self.cdn_url}{file_name}"
            print(f"Adding image {file_name} to the email body...")
            print(f"The image URL is: {file_url}")
            # round the precision to 2 decimal places
            #precision = round(detection.get_precision(), 2) if detection.get_precision() is not None else 0.0
            body += f"<p>Objeto to tipo {detection.get_label()} detectado em {detection.get_current_time()}.</p>"
            body += f'<img src="{file_url}" alt="{detection.get_label()}" style="max-width: 20%; height: auto;">'
            body += "<br>"
            # Add a line break between images
            body += "<hr>"
        body += "<p>Stay safe!</p>"
        return body

