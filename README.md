# 🎙️ FreeScribe — Free Speech-to-Text & OCR

**Stop paying for WhisperFlow, Otter.ai, and OCR APIs.**

FreeScribe is a 100% free, open-source, offline-first tool for:
- **Speech-to-Text** — Transcribe audio files (MP3, WAV, M4A, OGG, FLAC, WebM)
- **OCR** — Extract text from images (PNG, JPG, BMP, TIFF, PDF)

Everything runs **locally on your machine**. No API keys. No data sent anywhere. No usage limits.

## Why?

| Service | Monthly Cost | FreeScribe |
|---------|-------------|------------|
| WhisperFlow | $15-99/mo | $0 forever |
| Otter.ai | $17-40/mo | $0 forever |
| Google Cloud STT | $1.44/hr | $0 forever |
| Azure OCR | $1/1000 calls | $0 forever |
| Amazon Textract | $1.50/1000 pages | $0 forever |

## Features

- **Offline** — No internet needed after initial setup
- **Fast** — Uses faster-whisper (5x faster than OpenAI's whisper)
- **Multi-language** — 99 languages for STT, 100+ for OCR
- **CLI + Python API** — Use however you want
- **GPU optional** — Runs great on CPU, faster with GPU
- **Docker ready** — One command to deploy

## Quick Start

### Option 1: pip install (recommended)

```bash
pip install freescribe
```

### Option 2: From source

```bash
git clone https://github.com/YOUR_USERNAME/free-voice-ocr.git
cd free-voice-ocr
pip install -e .
```

### Option 3: Docker

```bash
docker run -p 5000:5000 freescribe/web
```

## Usage

### Command Line

```bash
# Transcribe audio
freescribe transcribe podcast.mp3
freescribe transcribe interview.wav --language en --model medium

# Extract text from image
freescribe ocr screenshot.png
freescribe ocr document.jpg --language spa

# Process entire folder
freescribe batch /path/to/audio/files/ --output transcripts/

# Launch web interface
freescribe serve
```

### Python API

```python
from freescribe import transcribe, ocr

# Speech to text
text = transcribe("audio.mp3", model="base", language="en")
print(text)

# OCR
text = ocr("image.png", language="eng")
print(text)
```

## Supported Formats

### Audio (Speech-to-Text)
MP3, WAV, M4A, OGG, FLAC, WMA, AAC, WebM, OPUS

### Images (OCR)
PNG, JPG/JPEG, BMP, TIFF, GIF, WebP, PDF

## Model Sizes

Choose your speed vs quality tradeoff:

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| tiny | 75MB | ⚡⚡⚡⚡⚡ | ⭐⭐ | Quick drafts |
| base | 150MB | ⚡⚡⚡⚡ | ⭐⭐⭐ | **Recommended** |
| small | 500MB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Good balance |
| medium | 1.5GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | High quality |
| large-v3 | 3GB | ⚡ | ⭐⭐⭐⭐⭐⭐ | Best possible |

## System Requirements

- **OS**: Linux, macOS, Windows
- **Python**: 3.8+
- **RAM**: 2GB minimum (4GB+ recommended)
- **Disk**: 500MB-5GB depending on model
- **GPU**: Optional (NVIDIA CUDA or Apple Silicon)

## Language Support

### Speech-to-Text (99 languages)
English, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Hindi, Portuguese, Russian, and 88 more. Auto-detected if not specified.

### OCR (100+ languages)
Install language packs:
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr-spa tesseract-ocr-fra tesseract-ocr-deu

# macOS
brew install tesseract-lang
```

## Docker Deployment

```dockerfile
# Dockerfile included
docker build -t freescribe .
docker run freescribe freescribe transcribe audio.mp3
```

## Contributing

We welcome contributions! Areas where help is needed:

- [ ] Real-time microphone transcription
- [ ] Batch processing improvements
- [ ] More language support
- [ ] Mobile app
- [ ] Browser extension
- [ ] GUI desktop app

## FAQ

**Q: Is this really free?**
A: Yes. MIT licensed. Forever free. No catch.

**Q: How accurate is it?**
A: Whisper (the underlying STT model) is near-human accuracy for English. OCR uses Tesseract, which handles clean documents very well.

**Q: Does it work offline?**
A: Yes. After downloading models (happens automatically on first use), no internet needed.

**Q: Can I use this commercially?**
A: Yes. MIT license means use it however you want.

**Q: What about private/confidential audio?**
A: Everything runs locally. Your data never leaves your machine.

## Star History

If this saves you money, star the repo! It helps others find it.

## License

MIT — Do whatever you want with it.

---

**Built with ❤️ by people who think transcription shouldn't cost money.**
