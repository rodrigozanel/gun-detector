# models/gun_detector.py
import cv2
import torch
from ultralytics import YOLO

class GunDetector:
    """
    A specialized detector that loads the YOLO model and processes frames
    to detect guns (or weapon-like objects). This class is solely responsible
    for detection.
    """
    def __init__(self, model_path, gun_class_ids, conf_threshold=0.55, gun_map=None, device=None):
        self.device = device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(model_path)
        self.model.to(self.device)
        self.gun_class_ids = gun_class_ids
        self.conf_threshold = conf_threshold
        self.gun_map = gun_map if gun_map is not None else {cid: f"Gun {cid}" for cid in gun_class_ids}

    def analyze_frame(self, frame):
        """
        Processes the frame, runs detection, and draws boxes/labels.
        
        :param frame: Input frame (numpy array).
        :return: Tuple of (processed_frame, detections) where detections is a list of dicts.
        """
        results = self.model.predict(frame, device=self.device, classes=self.gun_class_ids, conf=self.conf_threshold)
        detections = []

        for box in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, class_id = map(float, box)
            class_id_int = int(class_id)
            label = self.gun_map.get(class_id_int, f"Gun {class_id_int}")
            detections.append({
                'box': (int(x1), int(y1), int(x2), int(y2)),
                'confidence': conf,
                'class_id': class_id_int,
                'label': label,
            })
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            cv2.putText(frame, f"{label}: {conf * 100:.2f}%", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        return frame, detections
