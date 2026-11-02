import json
from pathlib import Path

DATA_DIR = Path("data")
SPLITS = {"Training": "train", "Validation": "val", "Testing": "test"}
EXCLUDE = {"VID30"}

# split folder Training, Validation Testing
# yolo split = train val test



video_dir = DATA_DIR / "Training" / "VID02"
    

json_path = video_dir / f"{video_dir.name}.json"

with open(json_path) as f:
    annotations = json.load(f)["annotations"]

missing = 0
for frame_id in annotations:
    image_path = video_dir / "Frames" / f"{int(frame_id):06d}.png"
    if not image_path.exists():
        missing += 1
    print(frame_id)

    boxes = annotations[frame_id]

    for box in boxes:
        class_id = box["instrument"]
        x, y, w, h = box["tool_bbox"]

        xc = x + w / 2
        yc = y + h / 2

        print(class_id, round(xc, 3), round(yc, 3), round(w, 3), round(h, 3))

    break

print(video_dir.name, len(annotations), "missing:", missing)
