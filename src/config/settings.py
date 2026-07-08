"""
קובץ קונפיגורציה מרכזי לפרויקט זיהוי פירות וירקות
"""
from pathlib import Path

# נתיבים
BASE_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = BASE_DIR / "best.pt"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"

# הגדרות מודל
MODEL_CONFIDENCE = 0.15
IMAGE_SIZE = 640

# נתוני פירות וירקות
AVERAGE_WEIGHT_GRAMS = {
    "broccoli": 350, "cabbage": 900, "carrot": 120, "cucumber": 250, "eggplant": 300,
    "paprika": 150, "potato": 180, "radish": 50, "tomato": 120, "apple": 180,
    "mango": 300, "orange": 200, "pear": 170, "watermelon": 4000, "banana": 120,
    "chili": 20, "avocado": 200, "beans": 5, "beet": 250, "cauliflower": 600,
    "celery": 100, "corn": 300, "garlic": 30, "onion": 150, "peas": 3,
    "pumpkin": 2500, "salad": 80, "cherry": 8, "grape": 5, "lemon": 80,
    "strawberry": 15, "nectarine": 140, "apricot": 50, "peach": 150,
}

REFERENCE_BOX_SIZE = {
    "broccoli": 220, "cabbage": 280, "carrot": 160, "cucumber": 200, "eggplant": 190,
    "paprika": 170, "potato": 165, "radish": 100, "tomato": 150, "apple": 170,
    "mango": 200, "orange": 185, "pear": 180, "watermelon": 350, "banana": 180,
    "chili": 80, "avocado": 180, "beans": 60, "beet": 200, "cauliflower": 250,
    "celery": 120, "corn": 220, "garlic": 90, "onion": 160, "peas": 50,
    "pumpkin": 300, "salad": 140, "cherry": 40, "grape": 35, "lemon": 140,
    "strawberry": 50, "nectarine": 160, "apricot": 110, "peach": 165,
}

HEBREW_NAMES = {
    "broccoli": "ברוקולי", "cabbage": "כרוב", "carrot": "גזר", "cucumber": "מלפפון", "eggplant": "חציל",
    "paprika": "פלפל", "potato": "תפוח אדמה", "radish": "צנון", "tomato": "עגבנייה", "apple": "תפוח",
    "mango": "מנגו", "orange": "תפוז", "pear": "אגס", "watermelon": "אבטיח", "banana": "בננה",
    "chili": "פלפל חריף", "avocado": "אבוקדו", "beans": "שעועית", "beet": "סלק", "cauliflower": "כרובית",
    "celery": "סלרי", "corn": "תירס", "garlic": "שום", "onion": "בצל", "peas": "אפונה",
    "pumpkin": "דלעת", "salad": "חסה", "cherry": "דובדבן", "grape": "ענבים", "lemon": "לימון",
    "strawberry": "תות", "nectarine": "נקטרינה", "apricot": "משמש", "peach": "אפרסק",
}

EMOJI = {
    "broccoli": "🥦", "cabbage": "🥬", "carrot": "🥕", "cucumber": "🥒", "eggplant": "🍆",
    "paprika": "🫑", "potato": "🥔", "radish": "🌱", "tomato": "🍅", "apple": "🍎",
    "mango": "🥭", "orange": "🍊", "pear": "🍐", "watermelon": "🍉", "banana": "🍌",
    "chili": "🌶️", "avocado": "🥑", "beans": "🫘", "beet": "🟣", "cauliflower": "🥬",
    "celery": "🌿", "corn": "🌽", "garlic": "🧄", "onion": "🧅", "peas": "🫛",
    "pumpkin": "🎃", "salad": "🥗", "cherry": "🍒", "grape": "🍇", "lemon": "🍋",
    "strawberry": "🍓", "nectarine": "🍑", "apricot": "🍑", "peach": "🍑",
}

# מחירים לק"ג (שקל)
PRICE_PER_KG = {
    "broccoli": 12.90, "cabbage": 4.50, "carrot": 3.90, "cucumber": 6.90, "eggplant": 8.90,
    "paprika": 15.90, "potato": 2.90, "radish": 5.90, "tomato": 7.90, "apple": 8.90,
    "mango": 19.90, "orange": 5.90, "pear": 12.90, "watermelon": 3.50, "banana": 6.90,
    "chili": 25.90, "avocado": 16.90, "beans": 18.90, "beet": 4.90, "cauliflower": 9.90,
    "celery": 8.90, "corn": 4.90, "garlic": 35.90, "onion": 2.90, "peas": 22.90,
    "pumpkin": 3.90, "salad": 7.90, "cherry": 29.90, "grape": 15.90, "lemon": 12.90,
    "strawberry": 24.90, "nectarine": 14.90, "apricot": 18.90, "peach": 16.90,
}