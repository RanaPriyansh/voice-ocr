"""
Basic usage examples for FreeScribe.
"""

from freescribe import transcribe, ocr


# Example 1: Simple transcription
print("=== Example 1: Transcribe audio ===")
# text = transcribe("podcast.mp3", language="en")
# print(text)


# Example 2: OCR on image
print("\n=== Example 2: OCR on image ===")
# text = ocr("screenshot.png")
# print(text)


# Example 3: Use Transcriber class for multiple files
print("\n=== Example 3: Transcriber class ===")
from freescribe import Transcriber

# Initialize once, use many times
transcriber = Transcriber(model="base")

# Transcribe multiple files without reloading model
# for audio_file in ["file1.mp3", "file2.wav", "file3.m4a"]:
#     segments = transcriber.transcribe(audio_file, language="en")
#     for seg in segments:
#         print(f"[{seg.start:.1f}s] {seg.text}")


# Example 4: Batch OCR
print("\n=== Example 4: Batch OCR ===")
from freescribe import OCR

ocr_engine = OCR(language="eng")

# Extract text from multiple images
# results = ocr_engine.extract_batch(["img1.png", "img2.jpg", "img3.bmp"])
# for path, result in results.items():
#     print(f"{path}: {result.text[:100]}...")
#     print(f"  Confidence: {result.confidence:.1f}%")


# Example 5: Save transcription to file
print("\n=== Example 5: Save to file ===")
from freescribe import transcribe_file

# transcribe_file("interview.mp3", "interview_transcript.txt", 
#                 model="base", language="en", timestamp=True)


# Example 6: Real-time streaming (for long files)
print("\n=== Example 6: Streaming transcription ===")
transcriber = Transcriber(model="base")

# for segment in transcriber.transcribe_streaming("long_podcast.mp3"):
#     print(f"[{segment.start:.1f}s - {segment.end:.1f}s] {segment.text}")


print("\nUncomment the examples above and provide real audio/image files to test!")
