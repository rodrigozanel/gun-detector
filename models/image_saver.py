# models/image_saver.py
import os
import cv2
from datetime import datetime

class ImageSaver:
    """
    Responsible for saving frames (images) to disk using a folder structure like:
    live/YYYY-MM-DD/HH/<label>
    """
    def __init__(self, base_folder="images/detections"):
        self.base_folder = base_folder

    def save_image(self, frame, label):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        #hour_str = now.strftime("%H%_M%_S")
        hour_str = f"{now.hour:02d}_{now.minute:02d}_{now.second:02d}"
        folder_path = os.path.join(self.base_folder, date_str, hour_str)
        os.makedirs(folder_path, exist_ok=True)
        filename = label + "_" + now.strftime("%Y%m%d_%H%M%S_%f") + ".jpg"
        file_path = os.path.join(folder_path, filename)
        cv2.imwrite(file_path, frame)
        return file_path
