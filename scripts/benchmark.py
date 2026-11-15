from pathlib import Path
from ultralytics import YOLO
import numpy as np

FRAMES_DIR = Path("data/Testing/VID01/Frames")

# sorted() puts frames in order (000526.png, 000551.png, ...); [:200] takes the first 200
image_paths = sorted(FRAMES_DIR.glob("*.png"))[:200]

print(f"Found {len(image_paths)} images")
print("First:", image_paths[0].name, "| Last:", image_paths[-1].name)

model_pytorch = YOLO("results/yolo11s_best.pt")

# for onnx need to specify task to detect
model_onnx = YOLO("results/yolo11s_best.onnx", task="detect")

for path in image_paths[:10]:
    model_pytorch.predict(path, imgsz=640, conf=0.25, verbose=False)
    model_onnx.predict(path, imgsz=640, conf=0.25, verbose=False)

speed_py = {}
speed_onnx = {}

speed_py["preprocess"] = []
speed_py["inference"] = []
speed_py["postprocess"] = []

speed_onnx["preprocess"] = []
speed_onnx["inference"] = []
speed_onnx["postprocess"] = []

for path in image_paths[:200]:

    results_py = model_pytorch.predict(path, imgsz=640, conf=0.25, verbose=False)
    
    speed_py["preprocess"].append(results_py[0].speed["preprocess"])
    speed_py["inference"].append(results_py[0].speed["inference"])
    speed_py["postprocess"].append(results_py[0].speed["postprocess"])

for path in image_paths[:200]:

    results_onnx = model_onnx.predict(path, imgsz=640, conf=0.25, verbose=False)

    speed_onnx["preprocess"].append(results_onnx[0].speed["preprocess"])
    speed_onnx["inference"].append(results_onnx[0].speed["inference"])
    speed_onnx["postprocess"].append(results_onnx[0].speed["postprocess"])

stages = ["preprocess", "inference", "postprocess"]

for s in stages:
    stages = ["preprocess", "inference", "postprocess"]

means_py = {}
means_onnx = {}
for s in stages:
    means_py[s] = np.mean(speed_py[s])
    means_onnx[s] = np.mean(speed_onnx[s])

total_py = sum(means_py.values())
fps_py = 1000 / total_py
total_onnx = sum(means_onnx.values())
fps_onnx = 1000 / total_onnx

print(f"py: pre {means_py['preprocess']:.1f}, inf {means_py['inference']:.1f}, post {means_py['postprocess']:.1f}, total {total_py}, fps {fps_py}")
print(f"onnx: pre {means_onnx['preprocess']:.1f}, inf {means_onnx['inference']:.1f}, post {means_onnx['postprocess']:.1f}, total {total_onnx}, fps {fps_onnx}")

p95_py = np.percentile(speed_py["inference"], 95)
p95_onnx = np.percentile(speed_onnx["inference"], 95)

# here you are getting the consistency of the model by getting the percentile
# showing spike and what not

print(f"py:   p95 inference {p95_py:.1f} ms")
print(f"onnx: p95 inference {p95_onnx:.1f} ms")


