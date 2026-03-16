# Changelog

All notable changes to FreeScribe will be documented here.

## [1.0.0] - 2026-03-16

### Added
- Initial release
- Speech-to-Text using faster-whisper (5x faster than OpenAI whisper)
- OCR using Tesseract 5.3
- CLI interface with `freescribe` command
- Python API for easy integration
- Web UI with drag-and-drop interface
- Batch processing support
- Support for 99 languages (STT) and 100+ languages (OCR)
- Docker support
- Streaming transcription for long files
- Model size selection (tiny to large-v3)
- Auto-detect language option
- Timestamp output option
- Confidence scores for OCR

### Features
- 100% offline after initial model download
- No API keys required
- No usage limits
- Runs on CPU (GPU optional)
- Cross-platform (Linux, macOS, Windows)
