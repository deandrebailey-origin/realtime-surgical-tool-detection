import json
from pathlib import Path

DATA_DIR = Path("data")
SPLITS = {"Training": "train", "Validation": "val", "Testing": "test"}
EXCLUDE = {"VID30"}

# split folder Training, Validation Testing
# yolo split = train val test



video_dir = DATA_DIR / "Validation" / "VID110"
    

json_path = video_dir / f"{video_dir.name}.json"

with open(json_path) as f:
    annotations = json.load(f)["annotations"]

missing = 0
for frame_id in annotations:
    image_path = video_dir / "Frames" / f"{int(frame_id):06d}.png"
    if not image_path.exists():
        missing += 1
    

    boxes = annotations[frame_id]

    for box in boxes:
        class_id = box["instrument"]
        x, y, w, h = box["tool_bbox"]

        if class_id == 5:
            print(frame_id)

        xc = x + w / 2
        yc = y + h / 2


print(video_dir.name, len(annotations), "missing:", missing)
