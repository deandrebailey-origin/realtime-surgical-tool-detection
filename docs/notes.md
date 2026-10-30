### Notes

YOLO is you need specific box format
- tool_bbox: [0.268, 0.429, 0.364, 0.196] confirms the format: normalized [x, y, w, h] with x, y at the top-left corner. That’s what you need for the converter.
- YOLO also needs one txt file per frame instead of the largjson
- Converter needs to find the box and shift box to the center
- Writes the format into one YOLO can understand
- And places it in a folder for YOLO to receive in teh correct structure