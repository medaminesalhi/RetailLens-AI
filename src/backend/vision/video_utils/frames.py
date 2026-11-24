"""Sample a video at approximately one frame per second."""
import math
from pathlib import Path
import cv2


def extract_frames(video_path, output_dir, max_frames=120):
    cap = cv2.VideoCapture(str(video_path))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    truncated = False
    try:
        if not cap.isOpened():
            raise ValueError("Impossible de lire la vidéo.")
        fps = cap.get(cv2.CAP_PROP_FPS)
        step = max(1, round(fps)) if math.isfinite(fps) and fps > 0 else 1
        index = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if index % step == 0:
                if len(saved) >= max_frames:
                    truncated = True
                    break
                path = output_dir / f"frame_{len(saved):04d}.jpg"
                if not cv2.imwrite(str(path), frame):
                    raise OSError("Could not save video frame")
                saved.append(path)
            index += 1
        if not saved:
            raise ValueError("Aucune image lisible dans la vidéo.")
        return saved, truncated
    finally:
        cap.release()
