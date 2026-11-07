import numpy as np
import cv2 as cv
import pathlib as Path

DATA_DIR = Path("data")
SPLITS = {"Training": "train"}

for split_folder, yolo_split in SPLITS.items():
    split_dir = DATA_DIR/ split_folder

    for video_dir in sorted(split_dir.iterdir()):
        if not video_dir.is_dir():
            continue

        

cap = cv.VideoCapture("data/Testing/VID01/VID01.mp4")
print("FPS:", cap.get(cv.CAP_PROP_FPS))
print("Frame Count:", cap.get(cv.CAP_PROP_FRAME_COUNT))
print("Width", cv.CAP_PROP_FRAME_WIDTH, "Height", cv.CAP_PROP_FRAME_HEIGHT)


cap.release()
cv.destroyAllWindows()
