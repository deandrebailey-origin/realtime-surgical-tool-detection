from ultralytics import YOLO

PATH = "data/Testing/VID01/Frames/000951.png"

model_pytorch = YOLO("results/yolo11s.pt")

# for onnx need to specify task to detect
model_onnx = YOLO("results/yolo11s.onnx", task="detect")

#verbose means? .predict() prints its own summary line for each image
results_py = model_pytorch.predict(PATH, imgsz=640, conf=0.25, verbose=False)
results_onnx = model_onnx.predict(PATH, imgsz=640, conf=0.25, verbose=False)

py_r = results_py[0].boxes
onnx_r = results_onnx[0].boxes

print("class", py_r.cls, onnx_r.cls)
print("conf", py_r.conf, onnx_r.conf)
print("xyxy", py_r.xyxy, onnx_r.xyxy)