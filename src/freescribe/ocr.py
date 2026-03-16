"""
OCR module using Tesseract.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# Supported image formats
IMAGE_FORMATS = {
    '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'
}


class OCRResult:
    """OCR result with text and optional confidence data."""
    
    def __init__(self, text: str, confidence: float = 0.0, 
                 word_boxes: Optional[List[Dict]] = None):
        self.text = text
        self.confidence = confidence
        self.word_boxes = word_boxes or []
    
    def __repr__(self):
        return f"OCRResult(confidence={self.confidence:.1f}%, text={self.text[:50]}...)"
    
    def __str__(self):
        return self.text


class OCR:
    """OCR engine using Tesseract."""
    
    def __init__(self, language: str = "eng"):
        """
        Initialize OCR engine.
        
        Args:
            language: Tesseract language code (eng, spa, fra, deu, etc)
        """
        try:
            import pytesseract
            from PIL import Image
        except ImportError as e:
            print(f"ERROR: Missing dependency: {e}")
            print("Install with: pip install pytesseract Pillow")
            sys.exit(1)
        
        self.language = language
        self.pytesseract = pytesseract
        self.Image = Image
    
    def extract(self, image_path: str, language: Optional[str] = None,
                config: str = "") -> OCRResult:
        """
        Extract text from image.
        
        Args:
            image_path: Path to image file
            language: Override default language
            config: Additional tesseract config string
        
        Returns:
            OCRResult with text and confidence
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        lang = language or self.language
        img = self.Image.open(image_path)
        
        # Get text
        text = self.pytesseract.image_to_string(img, lang=lang, config=config)
        
        # Get detailed data for confidence
        try:
            data = self.pytesseract.image_to_data(img, lang=lang, config=config, 
                                                  output_type=self.pytesseract.Output.DICT)
            
            # Calculate average confidence (excluding -1 values)
            confs = [int(c) for c in data['conf'] if int(c) > 0]
            avg_conf = sum(confs) / len(confs) if confs else 0
            
            # Build word boxes
            word_boxes = []
            for i in range(len(data['text'])):
                if data['text'][i].strip():
                    word_boxes.append({
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]),
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
        except Exception:
            avg_conf = 0
            word_boxes = []
        
        return OCRResult(
            text=text.strip(),
            confidence=avg_conf,
            word_boxes=word_boxes
        )
    
    def extract_batch(self, image_paths: List[str], 
                      language: Optional[str] = None) -> Dict[str, OCRResult]:
        """
        Extract text from multiple images.
        
        Returns dict mapping image path to OCRResult.
        """
        results = {}
        for path in image_paths:
            try:
                results[path] = self.extract(path, language=language)
            except Exception as e:
                results[path] = OCRResult(text=f"ERROR: {e}", confidence=0)
        return results
    
    def extract_pdf(self, pdf_path: str, language: Optional[str] = None,
                    dpi: int = 300) -> List[OCRResult]:
        """
        Extract text from PDF (converts pages to images first).
        
        Requires pdf2image: pip install pdf2image
        """
        try:
            from pdf2image import convert_from_path
        except ImportError:
            print("ERROR: pdf2image not installed.")
            print("Install with: pip install pdf2image")
            print("Also needs poppler: apt install poppler-utils")
            sys.exit(1)
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        pages = convert_from_path(str(pdf_path), dpi=dpi)
        results = []
        
        for page in pages:
            # Save temp image
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                page.save(f.name, 'PNG')
                result = self.extract(f.name, language=language)
                os.unlink(f.name)
                results.append(result)
        
        return results


# Global OCR instance
_ocr_engine = None


def _get_ocr(language: str = "eng") -> OCR:
    """Get or create global OCR instance."""
    global _ocr_engine
    if _ocr_engine is None or _ocr_engine.language != language:
        _ocr_engine = OCR(language=language)
    return _ocr_engine


def ocr(image_path: str, language: str = "eng", config: str = "") -> str:
    """
    Quick OCR function.
    
    Args:
        image_path: Path to image file
        language: Tesseract language code (eng, spa, fra, deu, etc)
        config: Additional tesseract config
    
    Returns:
        Extracted text
    
    Example:
        >>> from freescribe import ocr
        >>> text = ocr("screenshot.png")
        >>> print(text)
    """
    engine = _get_ocr(language)
    result = engine.extract(image_path, config=config)
    return result.text


def ocr_file(image_path: str, output_path: str, language: str = "eng",
             config: str = "") -> str:
    """
    OCR image and save to file.
    
    Returns the output file path.
    """
    text = ocr(image_path, language=language, config=config)
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    
    return str(output)
