"""
Utility functions for FreeScribe.
"""

from pathlib import Path
from typing import Set


def get_supported_audio_formats() -> Set[str]:
    """Return set of supported audio file extensions."""
    return {
        '.mp3', '.wav', '.m4a', '.ogg', '.flac', '.wma', '.aac', '.webm', '.opus', '.mp4'
    }


def get_supported_image_formats() -> Set[str]:
    """Return set of supported image file extensions."""
    return {
        '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'
    }


def is_audio_file(path: str) -> bool:
    """Check if path is a supported audio file."""
    return Path(path).suffix.lower() in get_supported_audio_formats()


def is_image_file(path: str) -> bool:
    """Check if path is a supported image file."""
    return Path(path).suffix.lower() in get_supported_image_formats()


def format_duration(seconds: float) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs:.1f}s"


def format_size(bytes_size: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"
