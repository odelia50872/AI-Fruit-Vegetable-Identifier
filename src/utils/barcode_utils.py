"""
barcode_utils.py — QR Code Generation for Detected Items

Generates a QR code image for a single detected fruit/vegetable,
embedding item metadata (name, quantity, weight, price) as JSON.
A text label strip is appended below the QR image for human readability.
"""
import qrcode
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
import io
import base64
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import HEBREW_NAMES, PRICE_PER_KG, EMOJI


def rtl(text):
    """
    Convert a Hebrew string to correct right-to-left display order for Pillow rendering.

    Pillow draws text left-to-right by default, so Hebrew strings must be
    reordered using the Unicode BiDi algorithm before drawing.

    Args:
        text: Any string (Hebrew or mixed).

    Returns:
        Visually reordered string suitable for Pillow's draw.text().
    """
    return get_display(str(text))


def generate_item_qr(class_name, quantity, total_weight, total_price):
    """
    Build a composite QR code + label image for a detected item.

    The QR code encodes a JSON payload with all item details so it can
    be scanned at a checkout terminal. A 70px label strip is appended
    below the QR image showing the item name, quantity, weight, and price.

    Args:
        class_name   : English item key (e.g. 'apple').
        quantity     : Number of detected units.
        total_weight : Combined estimated weight in grams.
        total_price  : Calculated price in ILS.

    Returns:
        (PIL.Image, dict) — the composite QR+label image and the embedded data dict.
    """
    # Build the JSON payload that will be encoded into the QR code
    data = {
        "name_he":      HEBREW_NAMES.get(class_name, class_name),
        "name_en":      class_name,
        "emoji":        EMOJI.get(class_name, "🍎"),
        "quantity":     quantity,
        "weight_grams": total_weight,
        "price_shekel": round(total_price, 2),
        "price_per_kg": PRICE_PER_KG.get(class_name, 0),
    }

    # Create the QR code object with low error correction (sufficient for short JSON)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2
    )
    qr.add_data(json.dumps(data, ensure_ascii=False))
    qr.make(fit=True)  # Auto-select the smallest version that fits the data

    # Render the QR code as an RGB PIL image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Append a text label strip below the QR image
    w, h = qr_img.size
    label_h = 70  # Height of the label area in pixels

    # Create a new white canvas tall enough for QR + label
    combined = Image.new("RGB", (w, h + label_h), "white")
    combined.paste(qr_img, (0, 0))  # Paste QR at the top

    draw = ImageDraw.Draw(combined)

    # Try to load a TrueType font; fall back to the built-in bitmap font
    try:
        font_big = ImageFont.truetype("arial.ttf", 15)
        font_sm  = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_big = font_sm = ImageFont.load_default()

    name_he = data["name_he"]

    # Draw three lines of text right-aligned inside the label strip
    # Line 1: emoji + Hebrew name
    draw.text(
        (w - 8, h + 4),
        rtl(f"{data['emoji']} {name_he}"),
        fill="black", font=font_big, anchor="rs"
    )
    # Line 2: quantity and weight
    draw.text(
        (w - 8, h + 24),
        rtl(f"כמות: {quantity}  |  משקל: {total_weight}g"),
        fill="#333", font=font_sm, anchor="rs"
    )
    # Line 3: total price and per-kg price (highlighted in red)
    draw.text(
        (w - 8, h + 42),
        rtl(f"מחיר: ₪{total_price:.2f}  |  לק\"ג: ₪{data['price_per_kg']}"),
        fill="#c00", font=font_sm, anchor="rs"
    )

    return combined, data


def image_to_base64(img):
    """
    Convert a PIL Image to a base64-encoded PNG string.

    Used to embed images directly in HTML <img> src attributes
    or Streamlit st.image() calls without writing to disk.

    Args:
        img: PIL Image object.

    Returns:
        Base64-encoded string of the PNG-encoded image.
    """
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
