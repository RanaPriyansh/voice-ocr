"""
FreeScribe — Free Speech-to-Text & OCR
100% offline, no API keys, no limits.
"""

__version__ = "1.0.0"

from .stt import transcribe, transcribe_file, Transcriber
from .ocr import ocr, ocr_file, OCR
from .utils import get_supported_audio_formats, get_supported_image_formats

__all__ = [
    "transcribe",
    "transcribe_file",
    "Transcriber",
    "ocr",
    "ocr_file",
    "OCR",
    "get_supported_audio_formats",
    "get_supported_image_formats",
]
