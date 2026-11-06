# Kaggle Setup

Zip the dataset into yolo_dataset.zip
- zip -r yolo_dataset.zip yolo -x "yolo/images/test/*" "yolo/labels/test/*"

Move the zip file into kaggle and name it what name you want it to be
- /kaggle/input/datasets/{username}/{your_dataset_name}/yolo/images/train/VID02_007001.png

```python

!pip install ultralytics

from pathlib import Path
yolo_root = Path("/kaggle/input/datasets/drebhd/cholectrack20-yolo/yolo").resolve()

yaml_text = f"""path: {yolo_root}
train: images/train
val: images/val
test: images/test
names: 
  0: grasper
  1: bipolar 
  2: hook 
  3: scissors 
  4: clipper 
  5: irrigator 
  6: specimen-bag
"""

with open("/kaggle/working/data.yaml", "w") as f:
    f.write(yaml_text)

print(yolo_root)

from ultralytics import YOLO
model = YOLO('yolo11s.pt')
model.train(data="/kaggle/working/data.yaml", epochs=40, imgsz=640, batch=32, project="/kaggle/working/runs")

```


The “background” column, grasper row (0.71): most false alarms are “grasper” predictions where no tool is labeled. Some may be real graspers that weren’t annotated, like the out-of-view area = 0 cases, and some are genuine mistakes. Worth a visual check.
Scissors → grasper (22%) and specimen-bag → grasper (14%): grasper is the most common class, so the model leans toward guessing it.
Hook (0.95), grasper (0.94), bipolar (0.90), clipper (0.90): strong.

None of that val_batch*_pred.jpeg contain irrigator but here is what i see in the labels .png not as much as the other but there are still a considerable amount that other tools also have around a similar amount

653 Training boxes for the irrigator tool and there is 88 in the validation set

Checking Frames

- 40851 slighly occluded
- 41201 slightly occluded and dark
- 46276 pretty visible
- 48301 Visible but dark

yolo detect predict model=results/best.pt source=data/Validation/VID110/Frames/040851.png conf=0.1 save=True
yolo detect predict model=results/best.pt source=data/Validation/VID110/Frames/041201.png conf=0.1 save=True
yolo detect predict model=results/best.pt source=data/Validation/VID110/Frames/046276.png conf=0.1 save=True
yolo detect predict model=results/best.pt source=data/Validation/VID110/Frames/048301.png conf=0.1 save=True