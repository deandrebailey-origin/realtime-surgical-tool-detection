import json
from pathlib import Path

DATA_DIR = Path("data")
SPLITS = {"Training": "train", "Validation": "val", "Testing": "test"}
EXCLUDE = {"VID30"}

# split folder Training, Validation Testing
# yolo split = train val test

for split_folder, yolo_split in SPLITS.items():
    split_dir = DATA_DIR / split_folder

    Path(f"yolo/labels/{yolo_split}").mkdir(parents=True, exist_ok=True)
    Path(f"yolo/images/{yolo_split}").mkdir(parents=True, exist_ok=True)

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
        
                xc = x + w / 2
                yc = y + h / 2
        
                lines.append(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")

            yolo_label_path = Path(f"yolo/labels/{yolo_split}/{frame_path}.txt")
            yolo_label_path.parent.mkdir(parents=True, exist_ok=True)

            with open(yolo_label_path, "w") as f:
                f.write("\n".join(lines))

            dest = Path(f"yolo/images/{yolo_split}/{frame_path}.png")
            if not dest.exists():
                dest.symlink_to(image_path.resolve())
        print(yolo_split, video_dir.name, len(annotations), "missing:", missing)
