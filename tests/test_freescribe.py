"""
Basic tests for FreeScribe.
"""

import pytest
import tempfile
import os
from pathlib import Path

from freescribe import (
    transcribe, ocr, 
    Transcriber, OCR,
    get_supported_audio_formats, get_supported_image_formats
)


class TestImports:
    """Test that all modules import correctly."""
    
    def test_import_stt(self):
        from freescribe.stt import Transcriber, Segment
        assert Transcriber is not None
        assert Segment is not None
    
    def test_import_ocr(self):
        from freescribe.ocr import OCR, OCRResult
        assert OCR is not None
        assert OCRResult is not None
    
    def test_import_cli(self):
        from freescribe.cli import main
        assert callable(main)
    
    def test_import_utils(self):
        from freescribe.utils import format_duration, format_size
        assert callable(format_duration)
        assert callable(format_size)


class TestFormats:
    """Test format detection."""
    
    def test_audio_formats(self):
        formats = get_supported_audio_formats()
        assert '.mp3' in formats
        assert '.wav' in formats
        assert '.ogg' in formats
        assert '.png' not in formats
    
    def test_image_formats(self):
        formats = get_supported_image_formats()
        assert '.png' in formats
        assert '.jpg' in formats
        assert '.mp3' not in formats


class TestTranscriber:
    """Test Transcriber class."""
    
    def test_transcriber_init(self):
        # Just test that it initializes without error
        transcriber = Transcriber(model="tiny")
        assert transcriber.model_name == "tiny"
        assert transcriber.model is not None
    
    def test_transcribe_nonexistent_file(self):
        transcriber = Transcriber(model="tiny")
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe("/nonexistent/file.mp3")


class TestOCR:
    """Test OCR class."""
    
    def test_ocr_init(self):
        engine = OCR(language="eng")
        assert engine.language == "eng"
    
    def test_ocr_nonexistent_file(self):
        engine = OCR(language="eng")
        with pytest.raises(FileNotFoundError):
            engine.extract("/nonexistent/image.png")


class TestUtils:
    """Test utility functions."""
    
    def test_format_duration(self):
        from freescribe.utils import format_duration
        assert "s" in format_duration(30.5)
        assert "m" in format_duration(90)
        assert "h" in format_duration(3700)
    
    def test_format_size(self):
        from freescribe.utils import format_size
        assert "B" in format_size(500)
        assert "KB" in format_size(1024)
        assert "MB" in format_size(1024 * 1024)
        assert "GB" in format_size(1024 * 1024 * 1024)


class TestSegment:
    """Test Segment class."""
    
    def test_segment_creation(self):
        from freescribe.stt import Segment
        seg = Segment(0.0, 5.0, "Hello world")
        assert seg.start == 0.0
        assert seg.end == 5.0
        assert seg.text == "Hello world"
    
    def test_segment_repr(self):
        from freescribe.stt import Segment
        seg = Segment(0.0, 5.0, "Hello world")
        assert "Segment" in repr(seg)
        assert "0.0s" in repr(seg)


class TestOCRResult:
    """Test OCRResult class."""
    
    def test_ocr_result_creation(self):
        from freescribe.ocr import OCRResult
        result = OCRResult("Hello world", confidence=95.5)
        assert result.text == "Hello world"
        assert result.confidence == 95.5
    
    def test_ocr_result_str(self):
        from freescribe.ocr import OCRResult
        result = OCRResult("Hello world")
        assert str(result) == "Hello world"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
