### Notes

YOLO is you need specific box format
- tool_bbox: [0.268, 0.429, 0.364, 0.196] confirms the format: normalized [x, y, w, h] with x, y at the top-left corner. That’s what you need for the converter.
- YOLO also needs one txt file per frame instead of the largjson
- Converter needs to find the box and shift box to the center
- Writes the format into one YOLO can understand
- And places it in a folder for YOLO to receive in teh correct structure

### Smoke Test

rm -rf yolo
python scripts/converter.py
cat yolo/data.yaml
yolo detect train data=yolo/data.yaml model=yolo11n.pt epochs=1 imgsz=640 batch=8 fraction=0.05 device=mps

### Results meaning?

Class	Val instances	What happened
grasper	1,180	Learning something (mAP50 0.24)
hook	1,054	Learning something (mAP50 0.23)
bipolar, clipper, irrigator, specimen-bag	77–219	~0. The model hasn’t learned them yet
scissors	23	~0, and very few examples to measure with

- Common Classes learned first
- Some classe samde no predictions for that class precision defualts to 1 while recal is 0
- Scissors only had 23 val examples scire will be noisy
- M4 ran 2.4 batches/sec. A full epoch (16,928 images ÷ 8) is about 2,100 batches, roughly 15 minutes per epoch for the smallest model.
- Best we if ran on kaggle because that way it'll be faster on Kaggle GPU

- Smoke test: YOLO11n, 1 epoch, 5% train → mAP50-95 0.033. Pipeline verified. Val (VID110) has all 7 classes; scissors only 23 instances.



