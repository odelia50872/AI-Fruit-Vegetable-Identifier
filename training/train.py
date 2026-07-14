"""
train.py — YOLOv8 Model Training Script (Google Colab)

Trains or resumes training of a YOLOv8s model on a custom
fruit/vegetable dataset stored in Google Drive.

Workflow:
  1. Mount Google Drive and locate the dataset ZIP file
  2. Extract the ZIP and find the data.yaml config
  3. Resume training from the latest checkpoint if one exists,
     otherwise start a fresh training run from scratch
  4. Save a checkpoint after every epoch for fault tolerance
"""

# =====================================================================
# Step 1: Mount Google Drive and locate the dataset ZIP
# =====================================================================
from google.colab import drive
import os
import zipfile
import glob

drive.mount('/content/drive')

# Automatically find any ZIP file in the root of Google Drive
zip_options = glob.glob('/content/drive/MyDrive/dataset.zip') + glob.glob('/content/drive/MyDrive/*.zip')

if not zip_options:
    raise FileNotFoundError("No ZIP file found in Google Drive. Please upload your dataset ZIP to My Drive.")

ZIP_PATH_IN_DRIVE = zip_options[0]
print(f"Found dataset ZIP: {ZIP_PATH_IN_DRIVE}")

LOCAL_EXTRACT_DIR = '/content/dataset_balanced'

# =====================================================================
# Step 2: Extract the ZIP and locate data.yaml
# =====================================================================
print("Extracting ZIP archive, please wait...")
with zipfile.ZipFile(ZIP_PATH_IN_DRIVE, 'r') as zip_ref:
    zip_ref.extractall(LOCAL_EXTRACT_DIR)
print("Extraction complete.")

# Recursively search for the YOLO dataset config file
yaml_search = glob.glob(f"{LOCAL_EXTRACT_DIR}/**/data.yaml", recursive=True)
if not yaml_search:
    raise FileNotFoundError("data.yaml not found inside the extracted ZIP.")

YAML_PATH = yaml_search[0]
print(f"Dataset config found: {YAML_PATH}")

# Directory in Drive where training checkpoints are backed up
DRIVE_BACKUP_DIR = '/content/drive/MyDrive/yolo_backup_results'
os.makedirs(DRIVE_BACKUP_DIR, exist_ok=True)

# =====================================================================
# Step 3: Install Ultralytics if needed, then train or resume
# =====================================================================
try:
    import ultralytics
except ImportError:
    !pip install ultralytics

from ultralytics import YOLO

# Look for the most recent checkpoint saved in Drive
backup_runs = glob.glob(f"{DRIVE_BACKUP_DIR}/yolo_balanced_run*/weights/last.pt")

if backup_runs:
    # Resume from the latest available checkpoint
    LAST_WEIGHTS_PATH = sorted(backup_runs)[-1]
    print(f"Resuming training from checkpoint: {LAST_WEIGHTS_PATH}")

    model = YOLO(LAST_WEIGHTS_PATH)

    # resume=True restores epoch count, optimizer state, and hyperparameters
    # save_period=1 ensures a checkpoint is written after every epoch
    results = model.train(
        resume=True,
        save_period=1
    )
else:
    # No checkpoint found — start a new training run from the pretrained base
    print("No checkpoint found. Starting fresh training run...")
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
        save_period=1      # Save a checkpoint after every epoch
    )
