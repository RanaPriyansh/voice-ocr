# Contributing to FreeScribe

Thank you for your interest in contributing! FreeScribe is a community project, and every contribution helps make free transcription accessible to everyone.

## Ways to Contribute

### 1. Report Bugs
Found something broken? Open an issue with:
- Your OS and Python version
- Steps to reproduce
- Error messages/logs
- Expected vs actual behavior

### 2. Suggest Features
Have an idea? We'd love to hear it! Open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you considered

### 3. Submit Code

#### Setup Development Environment

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/free-voice-ocr.git
cd free-voice-ocr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[all,dev]"
```

#### Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused

#### Submitting a PR

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### 4. Improve Documentation
- Fix typos or unclear explanations
- Add more examples
- Translate to other languages
- Write tutorials or blog posts

## Priority Areas

Here's where we especially need help:

### High Priority
- [ ] Real-time microphone transcription
- [ ] GUI desktop app (Electron/Tauri)
- [ ] Browser extension for video captions
- [ ] Batch processing performance improvements

### Medium Priority
- [ ] Support for more audio formats (via ffmpeg integration)
- [ ] Speaker diarization (who said what)
- [ ] Subtitle file generation (.srt, .vtt)
- [ ] Android/iOS apps

### Nice to Have
- [ ] Word-level timestamps
- [ ] Voice activity detection
- [ ] Custom vocabulary/boosting
- [ ] Integration with note-taking apps

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

Open an issue or start a discussion. We're friendly!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
