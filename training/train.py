זה קוד האימון, חשוב להוסיף אותו לקוד!!
# =====================================================================
# שלב 1: חיבור ל-Google Drive ובדיקת קבצים
# =====================================================================
from google.colab import drive
import os
import zipfile
import glob

drive.mount('/content/drive')

# --- בדיקה אוטומטית: מציאת קובץ ה-ZIP שלכן בדרייב ---
# הקוד יחפש כל קובץ ZIP שקיים בדרייב שלכן שמכיל את המילה dataset
zip_options = glob.glob('/content/drive/MyDrive/dataset.zip') + glob.glob('/content/drive/MyDrive/*.zip')

if not zip_options:
    raise FileNotFoundError("לא נמצא קובץ ZIP בדרייב. ודאו שהעליתן אותו לתיקייה הראשית בדרייב (My Drive)")

# בוחר את ה-ZIP הראשון שנמצא
ZIP_PATH_IN_DRIVE = zip_options[0]
print(f"נמצא קובץ ה-ZIP הבא בדרייב: {ZIP_PATH_IN_DRIVE}")

LOCAL_EXTRACT_DIR = '/content/dataset_balanced'

# =====================================================================
# שלב 2: חילוץ נקי
# =====================================================================
print("מחלץ את קובץ ה-ZIP... אנא המתינו...")
with zipfile.ZipFile(ZIP_PATH_IN_DRIVE, 'r') as zip_ref:
    zip_ref.extractall(LOCAL_EXTRACT_DIR)
print("החילוץ הסתיים!")

# --- איתור אוטומטי של קובץ ה-data.yaml שחולץ ---
yaml_search = glob.glob(f"{LOCAL_EXTRACT_DIR}/**/data.yaml", recursive=True)
if not yaml_search:
    raise FileNotFoundError("שגיאה: קובץ data.yaml לא נמצא בשום מקום בתוך ה-ZIP שחולץ!")

YAML_PATH = yaml_search[0]
print(f"קובץ התצורה נמצא בהצלחה בנתיב: {YAML_PATH}")

# תיקיית גיבוי קבועה בדרייב
DRIVE_BACKUP_DIR = '/content/drive/MyDrive/yolo_backup_results'
os.makedirs(DRIVE_BACKUP_DIR, exist_ok=True)
# =====================================================================
# שלב 3: המשך אימון המודל (Resume) ושמירה בכל אפוק
# =====================================================================
try:
    import ultralytics
except ImportError:
    !pip install ultralytics

from ultralytics import YOLO

# איתור אוטומטי של קובץ ה-last.pt בריצה האחרונה שלכן בדרייב
# הקוד מחפש את התיקייה האחרונה שנוצרה תחת yolo_balanced_run
import glob
backup_runs = glob.glob(f"{DRIVE_BACKUP_DIR}/yolo_balanced_run*/weights/last.pt")

if backup_runs:
    # לוקח את הריצה האחרונה שנמצאה (למשל yolo_balanced_run-3)
    LAST_WEIGHTS_PATH = sorted(backup_runs)[-1]
    print(f"🔄 נמצא קובץ גיבוי להמשך האימון בנתיב: {LAST_WEIGHTS_PATH}")

    # טעינת המודל מנקודת העצירה האחרונה
    model = YOLO(LAST_WEIGHTS_PATH)

    print("מתחיל בהמשך אימון המודל (Resume) ושמירה בכל אפוק בודד...")

    # בהמשך אימון (resume) מספיק להגדיר resume=True.
    # כדי לשנות את תדירות השמירה לכל אפוק, נוסיף גם את save_period=1
    results = model.train(
        resume=True,
        save_period=1
    )
else:
    print("⚠️ לא נמצא קובץ last.pt בדרייב. מתחיל אימון חדש מאפס...")
    model = YOLO('yolov8s.pt')

    results = model.train(
        data=YAML_PATH,
        epochs=60,
        imgsz=640,
        batch=64,
        device=0,
        project=DRIVE_BACKUP_DIR,
        name='yolo_balanced_run',
        save=True,
        save_period=1                 # שמירה בכל אפוק בודד מההתחלה
    )