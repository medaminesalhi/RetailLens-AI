from ..inference import detect


def run_yolo_on_frame(frame_path):
    categories, _ = detect(frame_path)
    return categories
