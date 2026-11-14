# export to multiple modes like ONNX and TensorRT

from ultralytics import YOLO

WEIGHTS = "results/yolo11s.pt"
EXPECTED = ["grasper", "bipolar", "hook", "scissors", "clipper", "irrigator", "specimen-bag"]

model = YOLO(WEIGHTS)


names = list(model.names.values())
print("Classes:", names)
if names != EXPECTED:
    raise SystemExit(f"Wrong weights: expected 7 tool classes, got {len(names)}. Re-download best.pt from Kaggle.")

path = model.export(format="onnx", imgsz=640, dynamic=False)
print("Saved:", path)

# dynamic allows for a flexible input shape but for ONNX and TensorRT off is simpler
# dynamic default is off
# for varying image sizes for example for this its 1 x 3 x 640 x 640
# faster because the runtime can plan memory for the input shape 

# a onnx file is a saved description of your netowrk
# showing everylayer and how they connect
# the top shows the models input: tensor: float32[1,3,640,640]
# the bottom shows the models output: tensor: float32[1,11,8400]

# 1    = batch size (one frame per run)
# 11   = values per box: 4 box values (x center, y center, width, height) + 7 class scores
# 8400 = candidate boxes (80x80 + 40x40 + 20x20 grid cells)

# raw output still needs: confidence threshold -> NMS -> rescale to original size
# non-maximum suppression which keeps the best box which is over the same tool
