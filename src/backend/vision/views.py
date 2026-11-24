"""REST endpoints for visual analysis and history."""
import logging
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .database import get_collection
from .services import analyze_image, analyze_video, InvalidMedia
from .storage import save_upload, media_url

logger = logging.getLogger(__name__)
IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".avi", ".mov", ".mkv"}


def validate_size(upload, megabytes):
    return 0 < upload.size <= megabytes * 1024 * 1024


@api_view(["POST"])
@parser_classes([MultiPartParser])
def process_image(request):
    upload = request.FILES.get("image")
    if not upload:
        return JsonResponse({"error": "Aucune image reçue."}, status=400)
    suffix = IMAGE_TYPES.get(upload.content_type)
    if not suffix:
        return JsonResponse({"error": "Format image non pris en charge."}, status=415)
    if not validate_size(upload, 10):
        return JsonResponse({"error": "Image vide ou supérieure à 10 Mio."}, status=413)
    path = None
    try:
        path, original_url = save_upload(upload, "images", suffix)
        output, categories, text = analyze_image(path)
        result = {"image_path": media_url(output.relative_to(Path(settings.MEDIA_ROOT))),
                  "categories": categories, "ocr_text": text}
        get_collection("image").insert_one({**result, "original_image_path": original_url,
            "date": timezone.now(), "source": request.POST.get("source", "unknown")})
        return JsonResponse(result)
    except InvalidMedia as exc:
        if path is not None:
            path.unlink(missing_ok=True)
        return JsonResponse({"error": str(exc)}, status=400)
    except Exception:
        logger.exception("Image analysis failed")
        return JsonResponse({"error": "Erreur interne lors de l'analyse."}, status=500)


@api_view(["POST"])
@parser_classes([MultiPartParser])
def process_video(request):
    upload = request.FILES.get("video")
    if not upload:
        return JsonResponse({"error": "Aucune vidéo reçue."}, status=400)
    suffix = Path(upload.name).suffix.lower()
    if suffix not in VIDEO_EXTENSIONS:
        return JsonResponse({"error": "Format vidéo non pris en charge."}, status=415)
    if not validate_size(upload, 100):
        return JsonResponse({"error": "Vidéo vide ou supérieure à 100 Mio."}, status=413)
    path = None
    try:
        path, url = save_upload(upload, "videos", suffix)
        frames, truncated = analyze_video(path, Path(settings.MEDIA_ROOT) / "frames" / path.stem)
        result = {"video_url": url, "frames": frames, "truncated": truncated}
        get_collection("video").insert_one({**result, "date": timezone.now()})
        return JsonResponse(result)
    except InvalidMedia as exc:
        if path is not None:
            path.unlink(missing_ok=True)
        return JsonResponse({"error": str(exc)}, status=400)
    except Exception:
        logger.exception("Video analysis failed")
        return JsonResponse({"error": "Erreur interne lors de l'analyse."}, status=500)


def history(kind, fields):
    try:
        docs = get_collection(kind).find().sort("date", -1).limit(50)
        results = []
        for doc in docs:
            item = {key: doc.get(key, default) for key, default in fields.items()}
            item.update(id=str(doc.get("_id", "")), date=doc.get("date", timezone.now()).isoformat())
            results.append(item)
        return JsonResponse(results, safe=False)
    except Exception:
        logger.exception("History lookup failed")
        return JsonResponse({"error": "Historique indisponible."}, status=503)


@api_view(["GET"])
def history_images(request):
    return history("image", {"image_path": "", "categories": [], "ocr_text": []})


@api_view(["GET"])
def history_videos(request):
    return history("video", {"video_url": "", "frames": [], "truncated": False})
