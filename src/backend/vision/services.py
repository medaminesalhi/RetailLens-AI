"""Image analysis independent of HTTP requests."""
from pathlib import Path
import cv2
from .inference import detect, read_text
from .utils.ocr_cleaner import nettoyer_et_corriger_ocr


class InvalidMedia(ValueError):
    pass


def analyze_image(path):
    image = cv2.imread(str(path))
    if image is None:
        raise InvalidMedia("Impossible de lire cette image.")
    categories, annotated = detect(image)
    filtered = cv2.bilateralFilter(image, 9, 75, 75)
    rgb = cv2.cvtColor(cv2.convertScaleAbs(filtered, alpha=1.2, beta=10), cv2.COLOR_BGR2RGB)
    results = read_text(rgb)
    raw = []
    for bbox, text, _ in results:
        if text.strip():
            raw.append(text)
            points = [(int(x), int(y)) for x, y in bbox]
            for start, end in zip(points, points[1:] + points[:1]):
                cv2.line(annotated, start, end, (0, 200, 0), 2)
    output = Path(path).with_name(Path(path).stem + "_annotated.jpg")
    if not cv2.imwrite(str(output), annotated):
        raise OSError("Could not save annotated image")
    return output, categories, nettoyer_et_corriger_ocr(raw)
