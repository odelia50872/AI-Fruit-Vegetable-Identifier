"""
yolo_model.py — YOLOv8 Model Wrapper

Provides the YOLOModel class which loads a trained YOLOv8 weights file
and exposes methods for standard inference and Top-K candidate prediction.
"""
import os
from ultralytics import YOLO
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import MODEL_PATH, MODEL_CONFIDENCE


class YOLOModel:
    """Wrapper around a trained YOLOv8 model for fruit/vegetable detection."""

    def __init__(self, model_path=None):
        """
        Initialize the model wrapper.

        Args:
            model_path: Optional path to a .pt weights file.
                        Defaults to MODEL_PATH from settings.
        """
        self.model_path = model_path or MODEL_PATH
        self.model = None                    # Will hold the loaded YOLO instance
        self.confidence = MODEL_CONFIDENCE   # Minimum confidence threshold for detections
        self.load_model()

    def load_model(self):
        """
        Load the YOLO weights file from self.model_path.

        Returns:
            True if the model loaded successfully, False otherwise.
        """
        try:
            if os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                return True
            else:
                print(f"Model file not found: {self.model_path}")
                return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def predict(self, image, conf=None):
        """
        Run standard YOLOv8 inference on a single image.

        Args:
            image: PIL Image or numpy array to run detection on.
            conf:  Optional confidence override. Uses self.confidence if not provided.

        Returns:
            YOLO results list, or None on failure.
        """
        if not self.model:
            return None

        confidence = conf or self.confidence
        try:
            results = self.model.predict(
                source=image,
                verbose=False,   # Suppress per-frame console output
                conf=confidence
            )
            return results
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    def predict_topk(self, image, k=3):
        """
        Run inference and return the top-k class candidates for each detected box.

        Strategy:
          1. Primary pass at self.confidence to get the main detections.
          2. Second low-threshold pass (conf=0.01, agnostic NMS) to collect
             all possible class scores across the image.
          3. For each primary box, find overlapping raw boxes (IoU > 0.3)
             and merge their class scores into a candidate dict.
          4. Return the top-k candidates per box sorted by confidence.

        Args:
            image: PIL Image or numpy array.
            k:     Number of top candidates to return per box (default 3).

        Returns:
            results      — standard YOLO results from the primary pass
            topk_per_box — list of lists; each inner list holds up to k dicts
                           with keys 'class', 'name', 'conf'
        """
        if not self.model:
            return None, []
        try:
            # --- Primary detection pass ---
            results = self.model.predict(source=image, verbose=False, conf=self.confidence)

            # Return early if no boxes were detected
            if not results or results[0].boxes is None or len(results[0].boxes) == 0:
                return results, []

            # --- Low-threshold pass to gather alternative class scores ---
            # agnostic_nms=True keeps boxes regardless of class overlap
            # max_det=300 ensures we capture many candidate boxes
            results_raw = self.model.predict(
                source=image, verbose=False,
                conf=0.01, agnostic_nms=True, max_det=300
            )

            topk_per_box = []

            for main_box in results[0].boxes:
                # Extract coordinates of the primary detection box
                mx1, my1, mx2, my2 = main_box.xyxy[0].tolist()
                main_cls  = int(main_box.cls[0])
                main_conf = float(main_box.conf[0])

                # Seed the candidate dict with the primary class
                candidates = {main_cls: main_conf}

                if results_raw and results_raw[0].boxes is not None:
                    for rb in results_raw[0].boxes:
                        rx1, ry1, rx2, ry2 = rb.xyxy[0].tolist()

                        # Compute intersection area between primary and raw box
                        ix1 = max(mx1, rx1); iy1 = max(my1, ry1)
                        ix2 = min(mx2, rx2); iy2 = min(my2, ry2)
                        inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)

                        if inter == 0:
                            continue  # No overlap — skip this raw box

                        # Compute IoU (Intersection over Union)
                        union = (mx2 - mx1) * (my2 - my1) + (rx2 - rx1) * (ry2 - ry1) - inter
                        iou = inter / union if union > 0 else 0

                        # Only consider raw boxes that significantly overlap the primary box
                        if iou > 0.3:
                            cls_id = int(rb.cls[0])
                            conf   = float(rb.conf[0])
                            # Keep the highest confidence score seen for each class
                            if cls_id not in candidates or conf > candidates[cls_id]:
                                candidates[cls_id] = conf

                # Sort all candidates by confidence and keep the top-k
                topk = sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:k]
                topk_per_box.append([
                    {"class": cid, "name": self.model.names.get(cid, ""), "conf": c}
                    for cid, c in topk
                ])

            return results, topk_per_box

        except Exception as e:
            print(f"Top-K prediction error: {e}")
            return None, []

    def get_model_info(self):
        """
        Return a summary dict of the loaded model's metadata.

        Returns:
            dict with keys 'model_path', 'names', 'confidence',
            or None if the model is not loaded.
        """
        if not self.model:
            return None

        return {
            "model_path": str(self.model_path),
            "names":      self.model.names,   # Dict mapping class id -> class name
            "confidence": self.confidence
        }
