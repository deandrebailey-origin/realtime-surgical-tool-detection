import json
from pathlib import Path

DATA_DIR = Path("data")
SPLITS = {"Validation": "val"}
EXCLUDE = {"VID30"}

# split folder Training, Validation Testing
# yolo split = train val test
irr = 0

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
            frame_path = f"{video_dir.name}_{int(frame_id):06d}"


            image_path = video_dir / "Frames" / f"{int(frame_id):06d}.png"
            if not image_path.exists():
                missing += 1
                continue

            boxes = annotations[frame_id]

            lines = []
            
            for box in boxes:
                class_id = box["instrument"]
                x, y, w, h = box["tool_bbox"]

                if class_id == 5:
                    irr += 1
        


print(irr)




