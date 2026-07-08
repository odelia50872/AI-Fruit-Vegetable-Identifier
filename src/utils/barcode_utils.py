"""
יצירת QR codes לפירות וירקות
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
    """המרת טקסט עברי להצגה נכונה מימין לשמאל ב-Pillow"""
    return get_display(str(text))


def generate_item_qr(class_name, quantity, total_weight, total_price):
    """יוצר תמונת QR עם פרטי פרי/ירק: שם, כמות, משקל, מחיר"""
    data = {
        "name_he": HEBREW_NAMES.get(class_name, class_name),
        "name_en": class_name,
        "emoji": EMOJI.get(class_name, "🍎"),
        "quantity": quantity,
        "weight_grams": total_weight,
        "price_shekel": round(total_price, 2),
        "price_per_kg": PRICE_PER_KG.get(class_name, 0),
    }

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
    qr.add_data(json.dumps(data, ensure_ascii=False))
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # הוספת פס טקסט מתחת ל-QR
    w, h = qr_img.size
    label_h = 70
    combined = Image.new("RGB", (w, h + label_h), "white")
    combined.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(combined)
    try:
        font_big = ImageFont.truetype("arial.ttf", 15)
        font_sm  = ImageFont.truetype("arial.ttf", 12)
    except:
        font_big = font_sm = ImageFont.load_default()

    name_he = data["name_he"]
    draw.text((w - 8, h + 4),  rtl(f"{data['emoji']} {name_he}"),                              fill="black", font=font_big, anchor="rs")
    draw.text((w - 8, h + 24), rtl(f"כמות: {quantity}  |  משקל: {total_weight}g"),             fill="#333",  font=font_sm,  anchor="rs")
    draw.text((w - 8, h + 42), rtl(f"מחיר: ₪{total_price:.2f}  |  לק\"ג: ₪{data['price_per_kg']}"), fill="#c00", font=font_sm, anchor="rs")

    return combined, data


def image_to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
