"""
Command-line interface for FreeScribe.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional


def main():
    parser = argparse.ArgumentParser(
        prog="freescribe",
        description="🎙️ FreeScribe — Free Speech-to-Text & OCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  freescribe transcribe podcast.mp3
  freescribe transcribe interview.wav --language en --model medium
  freescribe ocr screenshot.png
  freescribe ocr document.jpg --language spa
  freescribe batch /path/to/audio/ --output transcripts/
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe audio to text")
    transcribe_parser.add_argument("input", help="Audio file or directory")
    transcribe_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    transcribe_parser.add_argument("-m", "--model", default="base",
                                   choices=["tiny", "base", "small", "medium", "large-v3"],
                                   help="Model size (default: base)")
    transcribe_parser.add_argument("-l", "--language", help="Language code (auto-detect if not set)")
    transcribe_parser.add_argument("-t", "--timestamps", action="store_true",
                                   help="Include timestamps in output")
    transcribe_parser.add_argument("-d", "--device", default="cpu",
                                   choices=["cpu", "cuda", "auto"],
                                   help="Device to use (default: cpu)")
    
    # OCR command
    ocr_parser = subparsers.add_parser("ocr", help="Extract text from images")
    ocr_parser.add_argument("input", help="Image file or directory")
    ocr_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    ocr_parser.add_argument("-l", "--language", default="eng",
                           help="Tesseract language code (default: eng)")
    ocr_parser.add_argument("-c", "--config", default="",
                           help="Additional tesseract config")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process files")
    batch_parser.add_argument("input", help="Input directory")
    batch_parser.add_argument("-o", "--output", required=True, help="Output directory")
    batch_parser.add_argument("-m", "--model", default="base",
                             choices=["tiny", "base", "small", "medium", "large-v3"],
                             help="Model size for audio files")
    batch_parser.add_argument("-l", "--language", help="Language code")
    batch_parser.add_argument("-t", "--timestamps", action="store_true",
                             help="Include timestamps")
    
    # Version
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "transcribe":
        cmd_transcribe(args)
    elif args.command == "ocr":
        cmd_ocr(args)
    elif args.command == "batch":
        cmd_batch(args)


def cmd_transcribe(args):
    """Handle transcribe command."""
    from .stt import Transcriber, AUDIO_FORMATS
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize transcriber
    print(f"Loading {args.model} model...", file=sys.stderr)
    start = time.time()
    transcriber = Transcriber(model=args.model, device=args.device)
    load_time = time.time() - start
    print(f"Model loaded in {load_time:.1f}s", file=sys.stderr)
    
    # Transcribe
    print(f"Transcribing: {input_path}", file=sys.stderr)
    start = time.time()
    text = transcriber.transcribe_to_text(
        str(input_path),
        language=args.language,
        timestamp=args.timestamps
    )
    transcribe_time = time.time() - start
    
    print(f"Done in {transcribe_time:.1f}s", file=sys.stderr)
    
    # Output
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(text)


def cmd_ocr(args):
    """Handle OCR command."""
    from .ocr import OCR
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize OCR
    engine = OCR(language=args.language)
    
    # Extract text
    print(f"Extracting text from: {input_path}", file=sys.stderr)
    start = time.time()
    result = engine.extract(str(input_path), config=args.config)
    ocr_time = time.time() - start
    
    print(f"Done in {ocr_time:.1f}s (confidence: {result.confidence:.1f}%)", file=sys.stderr)
    
    # Output
    if args.output:
        Path(args.output).write_text(result.text, encoding="utf-8")
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(result.text)


def cmd_batch(args):
    """Handle batch command."""
    from .stt import Transcriber, AUDIO_FORMATS
    from .ocr import OCR, IMAGE_FORMATS
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.is_dir():
        print(f"ERROR: Not a directory: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find files
    audio_files = [f for f in input_dir.iterdir() 
                   if f.suffix.lower() in AUDIO_FORMATS]
    image_files = [f for f in input_dir.iterdir() 
                   if f.suffix.lower() in IMAGE_FORMATS]
    
    print(f"Found {len(audio_files)} audio files, {len(image_files)} image files", 
          file=sys.stderr)
    
    # Process audio
    if audio_files:
        print(f"\nLoading {args.model} model for audio...", file=sys.stderr)
        transcriber = Transcriber(model=args.model)
        
        for audio_file in audio_files:
            print(f"  Transcribing: {audio_file.name}", file=sys.stderr)
            out_file = output_dir / f"{audio_file.stem}.txt"
            text = transcriber.transcribe_to_text(
                str(audio_file),
                language=args.language,
                timestamp=args.timestamps
            )
            out_file.write_text(text, encoding="utf-8")
            print(f"    -> {out_file}", file=sys.stderr)
    
    # Process images
    if image_files:
        engine = OCR(language=args.language or "eng")
        
        for image_file in image_files:
            print(f"  OCR: {image_file.name}", file=sys.stderr)
            out_file = output_dir / f"{image_file.stem}.txt"
            result = engine.extract(str(image_file))
            out_file.write_text(result.text, encoding="utf-8")
            print(f"    -> {out_file} (confidence: {result.confidence:.1f}%)", 
                  file=sys.stderr)
    
    print(f"\nDone! Results in: {output_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
