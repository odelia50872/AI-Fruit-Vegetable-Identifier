"""
image_utils.py — Image Processing and Analysis Utilities

Provides helpers for:
  - Image quality validation (brightness, contrast, blur)
  - Weight estimation based on bounding-box size relative to class peers
  - Price calculation from weight and per-kg price table
  - Full analysis of YOLO detection results (counts, density, totals)
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
    """
    Validate image quality before running detection.

    Converts the image to grayscale and checks four quality criteria:
      - Brightness (mean pixel value): rejects too dark (<60) or too bright (>230)
      - Contrast (std deviation): rejects flat/low-contrast images (<15)
      - Sharpness (Laplacian variance): rejects blurry images (<20)

    Args:
        image: PIL Image object.

    Returns:
        (bool, str, str) — (is_ok, error_title, error_description)
    """
    # Convert to grayscale for luminance-based analysis
    gray = np.array(image.convert("L"))
    brightness = np.mean(gray)

    # Under-exposure check
    if brightness < 60:
        return False, "🌑 התמונה חשוכה מדי", "נסו לצלם עם תאורה טובה יותר."

    # Over-exposure check
    if brightness > 230:
        return False, "🌟 התמונה בהירה מדי", "נסו לצלם ללא אור חזק מדי."

    # Low contrast check — std dev measures spread of pixel intensities
    if np.std(gray) < 15:
        return False, "🎨 ניגודיות נמוכה", "קשה לזהות פריטים בתמונה זו."

    # Blur check — Laplacian variance drops sharply in blurry images
    if cv2.Laplacian(gray, cv2.CV_64F).var() < 20:
        return False, "🌫️ התמונה מטושטשת", "נסו לצלם תמונה חדה יותר."

    return True, "", ""


def calculate_price(class_name, weight_grams):
    """
    Calculate item price in ILS from weight in grams and the per-kg price table.

    Args:
        class_name:   English item key (e.g. 'apple').
        weight_grams: Estimated weight in grams.

    Returns:
        Price in ILS rounded to 2 decimal places.
    """
    price_per_kg = PRICE_PER_KG.get(class_name, 10.0)  # default fallback price
    weight_kg = weight_grams / 1000
    return round(price_per_kg * weight_kg, 2)


def estimate_weight(class_name, box_size_px, box_sizes_same_class=None):
    """
    Estimate item weight in grams using relative bounding-box size within its class.

    When multiple items of the same class are detected, their box sizes are
    compared to each other. The largest box is scaled to 115% of the average
    weight and the smallest to 85%, with linear interpolation in between.
    If only one item exists, the class average weight is returned directly.

    Args:
        class_name:           English item key.
        box_size_px:          Average of width+height of this item's bounding box (pixels).
        box_sizes_same_class: List of box sizes for all items of the same class.

    Returns:
        Estimated weight in grams (int).
    """
    base_weight = AVERAGE_WEIGHT_GRAMS.get(class_name, 150)

    # Single item — no relative comparison possible, return the class average
    if not box_sizes_same_class or len(box_sizes_same_class) == 1:
        return base_weight

    min_s, max_s = min(box_sizes_same_class), max(box_sizes_same_class)

    # All items are the same size — return the class average
    if max_s == min_s:
        return base_weight

    # Normalize box size to [0, 1] within the class group
    ratio = (box_size_px - min_s) / (max_s - min_s)

    # Map normalized ratio to a weight scale factor in [0.85, 1.15]
    factor = 0.85 + ratio * 0.30
    return round(base_weight * factor)


def analyze_image_results(results, model, topk_per_box=None, conf_threshold=0.15):
    """
    Parse YOLO detection results into structured per-class item data.

    For each detected box above conf_threshold:
      - Extracts bounding box coordinates and computes centroid + box size
      - Groups detections by class name
      - Merges Top-K alternative class candidates per box
      - Estimates per-item weight using relative box sizes within each class
      - Calculates per-item price
      - Computes spatial density from pairwise centroid distances

    Args:
        results:        YOLO results list from model.predict().
        model:          The underlying YOLO model (for class name lookup).
        topk_per_box:   Optional list of Top-K candidate dicts per box.
        conf_threshold: Minimum confidence to accept a detection (default 0.15).

    Returns:
        Tuple: (fruit_count, density, detected_items, total_weight, total_price)
          - fruit_count:    Total number of accepted detections.
          - density:        'high' / 'normal' / 'low' / 'single' / None.
          - detected_items: Dict keyed by class name with weights, prices, topk_merged.
          - total_weight:   Sum of all estimated weights (grams).
          - total_price:    Sum of all calculated prices (ILS).
    """
    fruit_count = 0
    detected_items = {}
    centroids  = []   # (cx, cy) for each accepted box — used for density calculation
    box_sizes  = []   # Average dimension of each accepted box
    total_price = 0

    # Guard: return zeros if results are empty or malformed
    if not results or len(results) == 0 or results[0].boxes is None:
        return 0, None, {}, 0, 0

    for i, box in enumerate(results[0].boxes):
        # Skip detections below the confidence threshold
        if float(box.conf[0]) < conf_threshold:
            continue

        fruit_count += 1

        # Extract pixel coordinates of the bounding box corners
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        # Compute centroid for density analysis
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        # Box size = average of width and height (used for weight estimation)
        box_size = ((x2 - x1) + (y2 - y1)) / 2

        centroids.append((cx, cy))
        box_sizes.append(box_size)

        class_name = model.names.get(int(box.cls[0]), "")

        # Skip classes not present in the weight lookup table
        if class_name not in AVERAGE_WEIGHT_GRAMS:
            continue

        # Initialize data structure for this class on first encounter
        if class_name not in detected_items:
            detected_items[class_name] = {
                'box_sizes':    [],
                'weights':      [],
                'prices':       [],
                'topk_merged':  {}   # Merged Top-K candidates: {class_name: best_conf}
            }

        detected_items[class_name]['box_sizes'].append(box_size)

        # Add the primary detection to the merged candidates dict
        main_conf = float(box.conf[0])
        merged = detected_items[class_name]['topk_merged']
        if class_name not in merged or main_conf > merged[class_name]:
            merged[class_name] = main_conf

        # Merge alternative Top-K candidates for this box (if available)
        if topk_per_box and i < len(topk_per_box):
            for candidate in topk_per_box[i]:
                cname = candidate['name']
                cconf = candidate['conf']
                # Keep the highest confidence seen for each alternative class
                if cname not in merged or cconf > merged[cname]:
                    merged[cname] = cconf

    # No valid detections found
    if fruit_count == 0:
        return 0, None, {}, 0, 0

    # --- Weight and price calculation ---
    # Uses relative box sizes within each class for proportional weight estimation
    for class_name, data in detected_items.items():
        box_sizes_cls = data['box_sizes']
        for bs in box_sizes_cls:
            w = estimate_weight(class_name, bs, box_sizes_cls)
            data['weights'].append(w)
            data['prices'].append(calculate_price(class_name, w))

    total_price  = sum(sum(item['prices'])  for item in detected_items.values())
    total_weight = sum(sum(item['weights']) for item in detected_items.values())

    # Single item — no density calculation needed
    if fruit_count == 1:
        return 1, "single", detected_items, total_weight, total_price

    # --- Spatial density calculation ---
    # Sum all pairwise Euclidean distances between centroids
    total_dist = sum(
        math.sqrt(
            (centroids[i][0] - centroids[j][0]) ** 2 +
            (centroids[i][1] - centroids[j][1]) ** 2
        )
        for i in range(len(centroids))
        for j in range(i + 1, len(centroids))
    )

    # Average pairwise distance divided by average box size gives a scale-independent ratio
    avg_pairwise_dist = total_dist / (len(centroids) * (len(centroids) - 1) / 2)
    avg_box_size      = sum(box_sizes) / len(box_sizes)
    ratio = avg_pairwise_dist / avg_box_size

    # Classify density based on empirically chosen thresholds
    density = "high" if ratio < 1.2 else "normal" if ratio < 2.2 else "low"

    return fruit_count, density, detected_items, total_weight, total_price
