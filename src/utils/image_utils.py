"""
פונקציות עזר לעיבוד תמונות ובדיקת איכות
"""
import numpy as np
import cv2
from PIL import Image
import math
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import AVERAGE_WEIGHT_GRAMS, PRICE_PER_KG


def check_image_quality(image):
    """בדיקת איכות התמונה"""
    gray = np.array(image.convert("L"))
    brightness = np.mean(gray)
    
    if brightness < 60:
        return False, "🌑 התמונה חשוכה מדי", "נסו לצלם עם תאורה טובה יותר."
    
    if brightness > 230:
        return False, "🌟 התמונה בהירה מדי", "נסו לצלם ללא אור חזק מדי."
    
    if np.std(gray) < 15:
        return False, "🎨 ניגודיות נמוכה", "קשה לזהות פריטים בתמונה זו."
    
    if cv2.Laplacian(gray, cv2.CV_64F).var() < 20:
        return False, "🌫️ התמונה מטושטשת", "נסו לצלם תמונה חדה יותר."
    
    return True, "", ""


def calculate_price(class_name, weight_grams):
    """חישוב מחיר לפי משקל"""
    price_per_kg = PRICE_PER_KG.get(class_name, 10.0)  # מחיר ברירת מחדל
    weight_kg = weight_grams / 1000
    return round(price_per_kg * weight_kg, 2)


def estimate_weight(class_name, box_size_px, box_sizes_same_class=None):
    """חישוב משקל משוער — דירוג יחסי בין פריטים מאותו סוג"""
    base_weight = AVERAGE_WEIGHT_GRAMS.get(class_name, 150)
    if not box_sizes_same_class or len(box_sizes_same_class) == 1:
        return base_weight
    min_s, max_s = min(box_sizes_same_class), max(box_sizes_same_class)
    if max_s == min_s:
        return base_weight
    # נרמול בין 0 ל-1 בתוך הקבוצה, ואז מיפוי ל-[0.85, 1.15] מהממוצע
    ratio = (box_size_px - min_s) / (max_s - min_s)
    factor = 0.85 + ratio * 0.30
    return round(base_weight * factor)


def analyze_image_results(results, model, topk_per_box=None, conf_threshold=0.15):
    """ניתוח תוצאות זיהוי התמונה"""
    fruit_count = 0
    detected_items = {}
    centroids = []
    box_sizes = []
    total_price = 0

    if not results or len(results) == 0 or results[0].boxes is None:
        return 0, None, {}, 0, 0

    for i, box in enumerate(results[0].boxes):
        if float(box.conf[0]) < conf_threshold:
            continue
            
        fruit_count += 1
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        box_size = ((x2 - x1) + (y2 - y1)) / 2
        centroids.append((cx, cy))
        box_sizes.append(box_size)
        
        class_name = model.names.get(int(box.cls[0]), "")
        if class_name not in AVERAGE_WEIGHT_GRAMS:
            continue

        if class_name not in detected_items:
            detected_items[class_name] = {'box_sizes': [], 'weights': [], 'prices': [], 'topk_merged': {}}

        detected_items[class_name]['box_sizes'].append(box_size)

        main_conf = float(box.conf[0])
        merged = detected_items[class_name]['topk_merged']
        if class_name not in merged or main_conf > merged[class_name]:
            merged[class_name] = main_conf

        # מוסיפים את שאר המועמדים מה-topk
        if topk_per_box and i < len(topk_per_box):
            for candidate in topk_per_box[i]:
                cname = candidate['name']
                cconf = candidate['conf']
                if cname not in merged or cconf > merged[cname]:
                    merged[cname] = cconf

    if fruit_count == 0:
        return 0, None, {}, 0, 0

    # חישוב משקלים לפי דירוג יחסי בתוך כל class
    for class_name, data in detected_items.items():
        box_sizes_cls = data['box_sizes']
        for bs in box_sizes_cls:
            w = estimate_weight(class_name, bs, box_sizes_cls)
            data['weights'].append(w)
            data['prices'].append(calculate_price(class_name, w))

    total_price = sum(sum(item['prices']) for item in detected_items.values())
    total_weight = sum(sum(item['weights']) for item in detected_items.values())

    if fruit_count == 1:
        return 1, "single", detected_items, total_weight, total_price

    # חישוב צפיפות
    total_dist = sum(
        math.sqrt((centroids[i][0]-centroids[j][0])**2 + 
                 (centroids[i][1]-centroids[j][1])**2)
        for i in range(len(centroids)) 
        for j in range(i+1, len(centroids))
    )
    
    ratio = (total_dist / (len(centroids)*(len(centroids)-1)/2)) / (sum(box_sizes)/len(box_sizes))
    density = "high" if ratio < 1.2 else "normal" if ratio < 2.2 else "low"
    
    return fruit_count, density, detected_items, total_weight, total_price