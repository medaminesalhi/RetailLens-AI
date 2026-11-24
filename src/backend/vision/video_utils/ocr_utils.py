import cv2
from ..inference import read_text


def run_ocr_on_frame(frame_path):
    image = cv2.imread(str(frame_path))
    if image is None:
        return []
    results = read_text(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return [text.strip() for _, text, _ in results if text.strip()]
