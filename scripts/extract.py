import numpy as np
import cv2 as cv
from pathlib import Path
import json
import numpy

DATA_DIR = Path("data")
SPLITS = {"Testing": "test"}

split_dir = DATA_DIR / "Testing"

for video_dir in sorted(split_dir.iterdir()):

    if not video_dir.is_dir():
        continue

    mp4_dir = video_dir / f"{video_dir.name}.mp4"

    
    # print("FPS:", cap.get(cv.CAP_PROP_FPS))
    # print("Frame Count:", cap.get(cv.CAP_PROP_FRAME_COUNT))
    # print("Width",   cap.get(cv.CAP_PROP_FRAME_WIDTH), "Height", cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    

    with open(video_dir / f"{video_dir.name}.json") as f:
         ids = sorted(int(k) for k in json.load(f)["annotations"])

    largest_id = ids[-1]

    id_set =set(ids)

    video_frame_path = video_dir / "Frames"
    video_frame_path.mkdir(exist_ok=True)

    #VideoCapture takes a string instead of a path
    cap = cv.VideoCapture(str(mp4_dir))

    frame_id = 0
    saved = 0
    while True:

        # ret bool for seeing if it returned anything and frame is the image itself
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id > largest_id:
            break

        # make the sorted ids into a set so i can check with in
        if frame_id in id_set:

            cv.imwrite(f"{video_frame_path}/{frame_id:06d}.png", frame)
            saved += 1

        frame_id += 1

        

    cap.release()

    print(f"{video_dir.name}: saved {saved} / expected {len(ids)}")

