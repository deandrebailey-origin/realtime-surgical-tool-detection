# Converter: CholecTrack20 → YOLO

Reference notes for `scripts/converter.py`: what it does, how, and why each decision was made.

## Goal

Turn CholecTrack20's per-video JSON labels into the format Ultralytics YOLO trains on.

| | CholecTrack20 (input) | YOLO (output) |
|---|---|---|
| Label files | One JSON per video | One `.txt` per image |
| Box format | `[x, y, w, h]`, normalized, **top-left** corner | `class x_center y_center w h`, normalized, **center** |
| Layout | `VIDxx/Frames/` + `VIDxx.json` | `images/{split}/` + matching `labels/{split}/` |
| Config | none | `data.yaml` (paths + class names) |

## Input

```
data/
  Training/    VID02, VID04, VID103, VID11, VID13, VID17, VID23, VID31, VID37, VID96
  Validation/  VID110, VID30 (excluded, see below)
  Testing/     VID01, VID06, VID07, VID111, VID12, VID25, VID39, VID92   (.mp4 only)
    VIDxx/
      Frames/006701.png ...      image name = frame ID, zero-padded to 6 digits
      VIDxx.json                 labels
```

JSON keys: `info`, `annotations`, `categories`, `video`.

- `annotations` is a dict: `"6701" → [box, box, ...]`. Keys are **strings**.
- Each box uses `instrument` (class ID) and `tool_bbox` (`[x, y, w, h]`). The rest (tracks, operator, phase, verb, target, triplet) is ignored for detection.
- `video` holds `width: 854`, `height: 480`. Boxes are already normalized, so the size isn't needed.
- Frame IDs step by **25** (25 fps video, labels at 1 fps).

## Classes

| ID | Name |
|---|---|
| 0 | grasper |
| 1 | bipolar |
| 2 | hook |
| 3 | scissors |
| 4 | clipper |
| 5 | irrigator |
| 6 | specimen-bag |

Confirmed from `categories["tools"]` in the JSON.

## Output

```
yolo/
  images/train/VID02_006701.png    (symlink to the original)
  labels/train/VID02_006701.txt
  images/val/...    labels/val/...
  images/test/...   labels/test/...
  data.yaml
```

## Steps

1. Map split folders to YOLO names: `Training → train`, `Validation → val`, `Testing → test`.
2. For each video folder: skip non-folders (`manifest.csv`, etc.) and anything in `EXCLUDE`.
3. Load `VIDxx.json` once and grab `["annotations"]`.
4. For each frame ID:
   - Image path: `Frames/{int(frame_id):06d}.png`. If it doesn't exist, count it and skip.
   - Output name: `{video}_{frame:06d}`.
5. For each box: `xc = x + w/2`, `yc = y + h/2`, keep `w` and `h`, and write `class xc yc w h`.
6. Write the `.txt` file, **even if it's empty**.
7. Symlink the image into `images/{split}/`.
8. Write `data.yaml`.
9. Print a summary: frames, boxes, empty frames, missing images, and boxes per class, for each split.

## Decisions and why

| Decision | Why |
|---|---|
| Prefix file names with the video (`VID02_006701`) | Frame numbers repeat across videos. Without the prefix, files overwrite each other. |
| Write empty `.txt` for frames with no boxes | Tells YOLO "no tools here" (background), which reduces false positives. |
| Symlink images instead of copying | Copying would duplicate 10+ GB on disk. |
| Skip labels whose image is missing | A label with no image can't be trained on. Report the count instead of failing. |
| Clip coordinates to 0–1 | Guards against boxes that go slightly past the image edge. |
| Exclude VID30 (`EXCLUDE = {"VID30"}`) | Its frames and labels are misaligned (see below). Wrong labels would penalize correct predictions. |
| Keep split by **video** (official split) | Frames from the same video are near-duplicates. Mixing them across splits leaks data and inflates scores. |

## Data issues found

**Missing images (labels with no frame on disk):**

| Video | Labels | Missing | Action |
|---|---|---|---|
| VID02 (train) | 2,545 | 1 | skip |
| VID31 (train) | 2,717 | 19 | skip |
| VID30 (val) | 1,066 | 318 | **video excluded** |
| Test set (all 8) | — | all | ships as `.mp4`, frames must be extracted |

**VID30 is excluded.**
- Image frame numbers run 11801–84776, while label IDs run 2876–34026. The ranges don't match.
- Visual checks: frame 13001 showed a hook box on empty tissue, with two visible tools unlabeled. Frame 26776 showed a hook box with no hook.
- Control: VID02 frame 6701 showed the box exactly on the scissors tip.
- Result: validation uses **VID110 only**. VID30 was never a training video, so no training data is lost.

**Annotation conventions to remember:**
- Boxes cover the **tooltip**, not the whole instrument shaft.
- Some boxes have `area: 0` and sit at the image edge (`y = 0`): the tool is mostly out of view. **Open question:** filter these? Count how common they are first.

## Validation checks

- Before converting: run `scripts/visualizer.py` on a few frames per split and confirm the boxes land on the tools.
- After converting: draw boxes from the **YOLO `.txt` files** on a few images. This checks the corner-to-center math.
- Check that VID110 has examples of every class. If a class is missing, consider moving one training video to val (still split by video).

## Open questions / next steps

- [ ] Filter `area == 0` boxes? Count them per split first.
- [ ] Check per-class box counts in train vs val.
- [ ] Write `scripts/extract_test_frames.py`: read each test `.mp4` **sequentially** with OpenCV and save only the labeled frame IDs as `Frames/{id:06d}.png`. Verify one frame with the visualizer.
- [ ] Add a COCO output mode later for RF-DETR.

## Environment

- Run inside the conda env: `conda activate surgtools`, then `python scripts/converter.py`.
- In VS Code, set the interpreter to **surgtools** (Cmd+Shift+P → Python: Select Interpreter). The default `/opt/homebrew/bin/python3` doesn't have OpenCV.
- `data/` and `yolo/` are gitignored. Never commit dataset images (CC BY-NC-SA, no redistribution).


