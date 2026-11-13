# goal

- the goal is to extract the videos into frames so that they can be tested
    - the files are currently placed in mp4 files   
    - its also important that these are only LABLED frames (no point in keeping frames with no boxes)

# notes

- OpenCV
    - with OpenCV you cant just jump to each frame which is stated within the annotations
    - jumping in compressed videos can land a few frames off
- turning the list of sorted id into a set allows for checking instantly instead of sequentially going through a list

