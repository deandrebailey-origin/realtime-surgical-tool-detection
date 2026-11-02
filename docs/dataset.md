## Label file format (`VIDxx.json`)

One JSON file per video. Top-level keys:

```json
{
  "info":        { ... },
  "annotations": { "<frame_id>": [ <box>, <box>, ... ], ... },
  "categories":  { "tools": [ ... ], "operators": [ ... ] },
  "video":       { "name": "VID02", "num_frames": 2545, "split": "training",
                   "height": 480, "width": 854 }
}
```

### `annotations`
- Dict of **frame ID (string) → list of boxes**, e.g. `"6701": [ ... ]`
- Frame IDs step by **25** (25 fps video, labeled at 1 fps)
- Image for a frame: `Frames/{int(frame_id):06d}.png` → `"6701"` = `006701.png`
- An empty list = no tools in that frame

### One box
```json
{
  "instrument": 3,
  "tool_bbox": [0.268, 0.429, 0.364, 0.196],
  "operator": 3,
  "phase": 0,
  "verb": -1, "target": -1, "triplet": -1,
  "intraoperative_track": 1,
  "intracorporeal_track": 1,
  "visibility_track": 1,
  "area": 47174.0,
  "score": 1.0,
  "iscrowd": 0,
  "visibility": 1, "visible": 1, "occluded": 0, "crowded": 0,
  "bleeding": 0, "smoke": 0, "blurred": 0,
  "undercoverage": 0, "reflection": 0, "stainedlens": 0
}
```

| Field | Meaning | Used for detection? |
|---|---|---|
| `instrument` | Class ID 0–6 | ✅ YOLO class |
| `tool_bbox` | `[x, y, w, h]`, normalized 0–1, **(x, y) = top-left corner** | ✅ Converted to center format |
| `area` | Box area in pixels. `0` = tool at the edge or out of view | ⚠️ Possible filter |
| `visible`, `occluded`, `blurred`, `smoke`, `bleeding`, ... | Per-box condition flags (0/1) | Optional filters or analysis |
| `operator` | Which hand holds the tool (see `categories.operators`) | ❌ |
| `phase` | Surgical phase | ❌ |
| `*_track` | Track IDs for tracking tasks | ❌ |
| `verb`, `target`, `triplet` | Action labels (-1 = unused here) | ❌ |
| `score`, `iscrowd` | COCO-style fields | ❌ |

### `categories`
- `tools`: 0 grasper, 1 bipolar, 2 hook, 3 scissors, 4 clipper, 5 irrigator, 6 specimen-bag
- `operators`: 0 null, 1 main surgeon left hand (MSLH), 2 assistant surgeon right hand (ASRH), 3 main surgeon right hand (MSRH)

- VID30 excluded. Image frame numbers (11801–84776) don’t match label frame IDs (2876–34026). Visual checks on frames 13001 and 26776 showed boxes on empty tissue and visible tools with no boxes. VID02 (control) aligned correctly. Validation uses VID110 only.