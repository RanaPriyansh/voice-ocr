"""
Speech-to-Text module using faster-whisper.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Iterator, List, Dict, Any

# Supported audio formats
AUDIO_FORMATS = {
    '.mp3', '.wav', '.m4a', '.ogg', '.flac', '.wma', '.aac', '.webm', '.opus', '.mp4'
}


class Segment:
    """A transcribed segment with timing information."""
    
    def __init__(self, start: float, end: float, text: str, 
                 avg_logprob: float = 0.0, no_speech_prob: float = 0.0):
        self.start = start
        self.end = end
        self.text = text
        self.avg_logprob = avg_logprob
        self.no_speech_prob = no_speech_prob
    
    def __repr__(self):
        return f"Segment({self.start:.1f}s-{self.end:.1f}s: {self.text[:50]}...)"


class Transcriber:
    """Main transcription class. Reuse for multiple files to avoid reloading model."""
    
    def __init__(self, model: str = "base", device: str = "cpu", 
                 compute_type: str = "int8"):
        """
        Initialize transcriber.
        
        Args:
            model: Model size (tiny, base, small, medium, large-v3)
            device: Device to use (cpu, cuda, auto)
            compute_type: Quantization (int8, float16, float32)
        """
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            print("ERROR: faster-whisper not installed.")
            print("Install with: pip install faster-whisper")
            sys.exit(1)
        
        self.model_name = model
        
        # Auto-detect best device
        if device == "auto":
            try:
                import torch
                if torch.cuda.is_available():
                    device = "cuda"
                    compute_type = "float16"
                elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    device = "cpu"  # MPS has issues with faster-whisper
                else:
                    device = "cpu"
            except ImportError:
                device = "cpu"
        
        self.model = WhisperModel(model, device=device, compute_type=compute_type)
        self.device = device
        self.compute_type = compute_type
    
    def transcribe(self, audio_path: str, language: Optional[str] = None,
                   **kwargs) -> List[Segment]:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            language: Language code (en, es, fr, etc). None for auto-detect.
            **kwargs: Additional faster-whisper parameters
        
        Returns:
            List of Segment objects with timing and text
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        segments_gen, info = self.model.transcribe(
            str(audio_path),
            language=language,
            **kwargs
        )
        
        segments = []
        for seg in segments_gen:
            segments.append(Segment(
                start=seg.start,
                end=seg.end,
                text=seg.text.strip(),
                avg_logprob=seg.avg_logprob,
                no_speech_prob=seg.no_speech_prob
            ))
        
        return segments
    
    def transcribe_to_text(self, audio_path: str, language: Optional[str] = None,
                          timestamp: bool = False, **kwargs) -> str:
        """
        Transcribe and return plain text.
        
        Args:
            audio_path: Path to audio file
            language: Language code
            timestamp: Include timestamps in output
            **kwargs: Additional parameters
        """
        segments = self.transcribe(audio_path, language=language, **kwargs)
        
        if timestamp:
            return "\n".join(
                f"[{s.start:.1f}s - {s.end:.1f}s] {s.text}" for s in segments
            )
        else:
            return " ".join(s.text for s in segments)
    
    def transcribe_streaming(self, audio_path: str, 
                            language: Optional[str] = None,
                            **kwargs) -> Iterator[Segment]:
        """
        Stream segments as they're transcribed.
        
        Yields Segment objects one at a time.
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        segments_gen, info = self.model.transcribe(
            str(audio_path),
            language=language,
            **kwargs
        )
        
        for seg in segments_gen:
            yield Segment(
                start=seg.start,
                end=seg.end,
                text=seg.text.strip(),
                avg_logprob=seg.avg_logprob,
                no_speech_prob=seg.no_speech_prob
            )


# Global transcriber instance (lazy loaded)
_transcriber = None


def _get_transcriber(model: str = "base") -> Transcriber:
    """Get or create global transcriber instance."""
    global _transcriber
    if _transcriber is None or _transcriber.model_name != model:
        _transcriber = Transcriber(model=model)
    return _transcriber


def transcribe(audio_path: str, model: str = "base", 
               language: Optional[str] = None,
               timestamp: bool = False, **kwargs) -> str:
    """
    Quick transcription function.
    
    Args:
        audio_path: Path to audio file
        model: Model size (tiny, base, small, medium, large-v3)
        language: Language code (en, es, fr, etc). None for auto-detect.
        timestamp: Include timestamps in output
        **kwargs: Additional faster-whisper parameters
    
    Returns:
        Transcribed text
    
    Example:
        >>> from freescribe import transcribe
        >>> text = transcribe("podcast.mp3", language="en")
        >>> print(text)
    """
    t = _get_transcriber(model)
    return t.transcribe_to_text(audio_path, language=language, 
                                timestamp=timestamp, **kwargs)


def transcribe_file(audio_path: str, output_path: str, model: str = "base",
                    language: Optional[str] = None,
                    timestamp: bool = True, **kwargs) -> str:
    """
    Transcribe audio and save to file.
    
    Returns the output file path.
    """
    text = transcribe(audio_path, model=model, language=language,
                      timestamp=timestamp, **kwargs)
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    
    return str(output)
