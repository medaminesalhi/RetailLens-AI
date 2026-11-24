from django.test import SimpleTestCase
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from .utils.ocr_cleaner import nettoyer_et_corriger_ocr


class OCRTests(SimpleTestCase):
    def test_preserves_prices_and_arabic(self):
        self.assertEqual(nettoyer_et_corriger_ocr(["  Promo  20% ", "حليب", "Promo 20%", " "]), ["Promo 20%", "حليب"])


class UploadTests(SimpleTestCase):
    def test_missing_image(self):
        self.assertEqual(self.client.post("/api/process-image/").status_code, 400)

    def test_missing_video(self):
        self.assertEqual(self.client.post("/api/process-video/").status_code, 400)

    def test_unsupported_image(self):
        upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
        self.assertEqual(self.client.post("/api/process-image/", {"image": upload}).status_code, 415)

    @patch("vision.views.get_collection")
    def test_image_history_empty(self, collection):
        collection.return_value.find.return_value.sort.return_value.limit.return_value = []
        response = self.client.get("/api/history-images/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
