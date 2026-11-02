import json
from pathlib import Path

video_dir = Path("data/Validation/VID30")

with open(video_dir / "VID30.json") as f:
    labels = sorted(int(k) for k in json.load(f)["annotations"])

images = sorted(int(p.stem) for p in (video_dir / "Frames").glob("*.png"))
image_set = set(images)
missing = [fid for fid in labels if fid not in image_set]

print("labels:  first", labels[:5], "last", labels[-5:])
print("images:  first", images[:5], "last", images[-5:])
print("missing: count", len(missing), "first", missing[:10], "last", missing[-5:])