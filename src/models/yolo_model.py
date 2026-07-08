"""
מחלקה לניהול מודל YOLO
"""
import os
from streamlit import image
from ultralytics import YOLO
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import MODEL_PATH, MODEL_CONFIDENCE


class YOLOModel:
    def __init__(self, model_path=None):
        self.model_path = model_path or MODEL_PATH
        self.model = None
        self.confidence = MODEL_CONFIDENCE
        self.load_model()
    
    def load_model(self):
        """טעינת המודל"""
        try:
            if os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                return True
            else:
                print(f"❌ קובץ המודל לא נמצא: {self.model_path}")
                return False
        except Exception as e:
            print(f"❌ שגיאה בטעינת המודל: {e}")
            return False
    
    def predict(self, image, conf=None):
        """זיהוי פריטים בתמונה"""
        if not self.model:
            return None
        
        confidence = conf or self.confidence
        try:
            results = self.model.predict(
                source=image, 
                verbose=False, 
                conf=confidence
            )
            return results
        except Exception as e:
            print(f"❌ שגיאה בחיזוי: {e}")
            return None

    def predict_topk(self, image, k=3):
        """זיהוי עם Top-K אפשרויות לכל פריט — לפי IoU חפיפה אמיתית"""
        if not self.model:
            return None, []
        try:
            results = self.model.predict(source=image, verbose=False, conf=self.confidence)
            if not results or results[0].boxes is None or len(results[0].boxes) == 0:
                return results, []

            # הרצה עם conf נמוך + agnostic_nms=True כדי לקבל כל class לכל מיקום
            results_low = self.model.predict(source=image, verbose=False, conf=0.05, agnostic_nms=False, max_det=1000)
            topk_per_box = []
            for main_box in results[0].boxes:
                mx1, my1, mx2, my2 = main_box.xyxy[0].tolist()
                main_cls  = int(main_box.cls[0])
                main_conf = float(main_box.conf[0])

                candidates = {main_cls: main_conf}

                if results_low and results_low[0].boxes is not None:
                    for rb in results_low[0].boxes:
                        rx1, ry1, rx2, ry2 = rb.xyxy[0].tolist()

                        # חישוב IoU — רק boxes שחופפים ממש הם אותו אובייקט
                        ix1, iy1 = max(mx1, rx1), max(my1, ry1)
                        ix2, iy2 = min(mx2, rx2), min(my2, ry2)
                        inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
                        if inter == 0:
                            continue
                        union = (mx2-mx1)*(my2-my1) + (rx2-rx1)*(ry2-ry1) - inter
                        iou = inter / union if union > 0 else 0

                        if iou > 0.4:  # חפיפה משמעותית = אותו אובייקט
                            cls_id = int(rb.cls[0])
                            conf   = float(rb.conf[0])
                            if cls_id not in candidates or conf > candidates[cls_id]:
                                candidates[cls_id] = conf

                topk = sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:k]
                topk_per_box.append([
                    {"class": cls_id, "name": self.model.names.get(cls_id, ""), "conf": conf}
                    for cls_id, conf in topk
                ])

            return results, topk_per_box
        except Exception as e:
            print(f"❌ שגיאה בחיזוי Top-K: {e}")
            return None, []

    def get_model_info(self):
        """מידע על המודל"""
        if not self.model:
            return None
        
        return {
            "model_path": str(self.model_path),
            "names": self.model.names,
            "confidence": self.confidence
        }