"""Load each model on demand and serialize access within a process."""
import os
from pathlib import Path
from threading import RLock

_lock = RLock()
_yolo = None
_ocr = None


def detect(image):
    global _yolo
    with _lock:
        if _yolo is None:
            from ultralytics import YOLO
            _yolo = YOLO(str(Path(__file__).with_name("best.pt")))
        result = _yolo(image, device=os.getenv("YOLO_DEVICE", "cpu"), verbose=False)[0]
        ids = result.boxes.cls.tolist() if result.boxes is not None else []
        return sorted({_yolo.names[int(cid)] for cid in ids}), result.plot()


def read_text(image):
    global _ocr
    with _lock:
        if _ocr is None:
            import easyocr
            _ocr = easyocr.Reader(["en", "ar"], gpu=os.getenv("OCR_GPU", "false").lower() == "true")
        return _ocr.readtext(image)
