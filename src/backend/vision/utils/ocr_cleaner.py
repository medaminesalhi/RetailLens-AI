"""Normalize OCR without guessing brand names or changing numbers."""
import re
import unicodedata


def nettoyer_texte_ocr_brut(texte):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", texte)).strip()


def nettoyer_et_corriger_ocr(ocr_list):
    cleaned = (nettoyer_texte_ocr_brut(text) for text in ocr_list)
    return list(dict.fromkeys(text for text in cleaned if text))
