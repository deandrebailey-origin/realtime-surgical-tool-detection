# Real-Time Surgical Tool Detection

Detecting surgical instruments in laparoscopic surgery video, then making the detector fast enough for real time: **YOLO → ONNX → TensorRT → C++**.

Built on the [CholecTrack20](https://github.com/camma-public/cholectrack20) dataset: 20 laparoscopic cholecystectomy (gallbladder removal) videos, annotated at 1 fps with 7 tool classes.

> **Status:** 🚧 In progress. The data pipeline is complete and verified end to end. Baseline training is next.

---

## Why

Knowing which tools are in use, and where, is a building block for surgical workflow analysis, skill assessment, and AI assistance in the operating room. For any of that to be useful *during* surgery, the model has to be both **accurate** and **fast**. This project covers both: a careful, honestly evaluated detector, and an optimized inference path for real-time use.

## Pipeline

```
CholecTrack20 (JSON labels + frames)
        │  scripts/converter.py
        ▼
YOLO format (labels + data.yaml)
        │  Ultralytics YOLO11
        ▼
Trained detector (.pt)
        │  export
        ▼
ONNX  ──►  TensorRT engine (FP16 / INT8)  ──►  C++ inference app
```

## Progress

- [x] Download the dataset and document its format ([docs/dataset.md](docs/dataset.md))
- [x] Write a converter from CholecTrack20 JSON to YOLO format ([docs/converter.md](docs/converter.md))
- [x] Verify labels visually and audit data quality
- [x] Smoke-test training (YOLO11n, 1 epoch): the pipeline works end to end
- [ ] Train a baseline YOLO11s and report per-class results
- [ ] Extract test-set frames from video and run the final evaluation
- [ ] Export to ONNX and benchmark with ONNX Runtime
- [ ] Build a TensorRT engine (FP16 / INT8) and compare latency and accuracy
- [ ] C++ inference application
- [ ] Latency table: PyTorch vs. ONNX Runtime vs. TensorRT

## Data

| Split | Videos | Labeled frames used |
|---|---|---|
| Train | 10 | 16,928 |
| Val | 1 (VID110) | 1,713 |
| Test | 8 | *(extracted from `.mp4`; pending)* |

**Classes:** grasper, bipolar, hook, scissors, clipper, irrigator, specimen-bag

### Data-quality decisions

Every decision and the evidence behind it is recorded in [docs/converter.md](docs/converter.md). The main ones:

- **Splits are by video**, following the official split. Frames from the same video are near-duplicates, so mixing them across splits would leak data and inflate scores.
- **VID30 is excluded.** Its image frame numbers (11,801–84,776) don't match its label IDs (2,876–34,026). Visual checks showed boxes on empty tissue and visible tools left unlabeled. A control video (VID02) aligned correctly. Validation therefore uses VID110, which still contains all 7 classes.
- **Labels with missing images are skipped** (20 in train) and reported rather than silently dropped.
- **The test set ships as video,** so frames are extracted at the labeled frame IDs.
- **Boxes cover tool tips,** not whole instruments, so predictions should be read the same way.

## Results

*Coming soon: baseline mAP@50 and mAP@50-95 per class, plus a latency comparison across inference backends.*

## Run it

```bash
# Environment
conda create -n surgtools python=3.11 -y
conda activate surgtools
pip install ultralytics opencv-python matplotlib synapseclient

# 1. Download CholecTrack20 (requires an approved access request + Synapse token)
export CHOLECTRACK_ACCESS_KEY="..."      # from the dataset approval email
python scripts/download_cholec.py

# 2. Convert to YOLO format (writes yolo/ with labels, image symlinks, data.yaml)
python scripts/converter.py

# 3. Train
yolo detect train data=yolo/data.yaml model=yolo11s.pt epochs=50 imgsz=640
```

Secrets are never stored in code. Synapse login uses `~/.synapseConfig`, and the access key comes from an environment variable.

## Project structure

```
scripts/
  download_cholec.py   download from Synapse (no secrets in code)
  converter.py         CholecTrack20 JSON → YOLO labels + data.yaml
  visualizer.py        draw ground-truth boxes to verify labels
docs/
  dataset.md           dataset format and label fields
  converter.md         conversion plan, decisions, and data issues
data/                  dataset (gitignored)
yolo/                  generated YOLO dataset (gitignored)
runs/                  training outputs (gitignored)
```

## Data license

CholecTrack20 is released under **CC BY-NC-SA 4.0** by CAMMA (University of Strasbourg). This repository contains **code only**: no images, videos, labels, or trained weights derived from the dataset are distributed here.

> C.I. Nwoye et al., "CholecTrack20: A Multi-Perspective Tracking Dataset for Surgical Tools," CVPR 2025.

## Author

**DeAndre Bailey**, Computer Science, University of Central Florida
