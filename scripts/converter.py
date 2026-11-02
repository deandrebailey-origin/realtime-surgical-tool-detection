import json
from pathlib import Path

DATA_DIR = Path("data")
SPLITS = {"Training": "train", "Validation": "val", "Testing": "test"}
EXCLUDE = {"VID30"}

# split folder Training, Validation Testing
# yolo split = train val test

for split_folder, yolo_split in SPLITS.items():
    split_dir = DATA_DIR / split_folder

    for video_dir in sorted(split_dir.iterdir()):
        if not video_dir.is_dir():
            continue

        if video_dir.name in EXCLUDE:
            continue
            

        json_path = video_dir / f"{video_dir.name}.json"

        with open(json_path) as f:
            annotations = json.load(f)["annotations"]

        missing = 0
        for frame_id in annotations:
            image_path = video_dir / "Frames" / f"{int(frame_id):06d}.png"
            if not image_path.exists():
                missing += 1

        print(yolo_split, video_dir.name, len(annotations), "missing:", missing)
