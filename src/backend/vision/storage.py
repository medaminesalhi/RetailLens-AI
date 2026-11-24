from pathlib import Path
from uuid import uuid4
from django.conf import settings


def save_upload(upload, directory, suffix):
    relative = Path(directory) / f"{uuid4().hex}{suffix}"
    path = Path(settings.MEDIA_ROOT) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        for chunk in upload.chunks():
            handle.write(chunk)
    return path, media_url(relative)


def media_url(relative):
    return settings.MEDIA_URL.rstrip("/") + "/" + Path(relative).as_posix()
