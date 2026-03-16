"""
Web interface for FreeScribe.
Simple drag-and-drop UI for transcription and OCR.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

try:
    from flask import Flask, request, jsonify, render_template_string
except ImportError:
    raise ImportError("Flask not installed. Install with: pip install flask")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FreeScribe — Free Speech-to-Text & OCR</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 2rem;
        }
        .container { max-width: 900px; margin: 0 auto; }
        h1 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 2rem;
        }
        .tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .tab {
            flex: 1;
            padding: 1rem;
            background: #1a1a1a;
            border: 2px solid #333;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            font-size: 1rem;
            color: #aaa;
            transition: all 0.2s;
        }
        .tab:hover { border-color: #555; color: #fff; }
        .tab.active {
            border-color: #00d4ff;
            background: #1a2a3a;
            color: #00d4ff;
        }
        .dropzone {
            border: 3px dashed #333;
            border-radius: 12px;
            padding: 3rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 1.5rem;
        }
        .dropzone:hover, .dropzone.dragover {
            border-color: #00d4ff;
            background: #1a2a3a;
        }
        .dropzone-icon { font-size: 3rem; margin-bottom: 1rem; }
        .dropzone-text { color: #888; }
        .dropzone-text strong { color: #00d4ff; }
        .options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .option {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 1rem;
        }
        .option label {
            display: block;
            color: #888;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
        }
        .option select, .option input {
            width: 100%;
            background: #0f0f0f;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 0.5rem;
            color: #e0e0e0;
            font-size: 1rem;
        }
        .btn {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #00d4ff, #7c3aed);
            border: none;
            border-radius: 8px;
            color: #000;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .btn:hover { opacity: 0.9; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .result {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            display: none;
        }
        .result.visible { display: block; }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .result-title { font-size: 1.1rem; font-weight: bold; }
        .result-meta { color: #888; font-size: 0.85rem; }
        .result-text {
            background: #0f0f0f;
            border-radius: 4px;
            padding: 1rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'SF Mono', 'Fira Code', monospace;
            font-size: 0.9rem;
            line-height: 1.6;
        }
        .copy-btn {
            background: #333;
            border: 1px solid #555;
            border-radius: 4px;
            color: #e0e0e0;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 0.85rem;
        }
        .copy-btn:hover { background: #444; }
        .loading {
            text-align: center;
            padding: 2rem;
            display: none;
        }
        .loading.visible { display: block; }
        .spinner {
            border: 3px solid #333;
            border-top: 3px solid #00d4ff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .error {
            background: #3a1a1a;
            border: 1px solid #ff4444;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            color: #ff8888;
            display: none;
        }
        .error.visible { display: block; }
        .footer {
            text-align: center;
            color: #555;
            margin-top: 3rem;
            font-size: 0.85rem;
        }
        .footer a { color: #00d4ff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ FreeScribe</h1>
        <p class="subtitle">Free, offline Speech-to-Text & OCR. No API keys. No limits.</p>
        
        <div class="tabs">
            <div class="tab active" data-mode="transcribe">🎤 Speech-to-Text</div>
            <div class="tab" data-mode="ocr">📷 OCR (Image → Text)</div>
        </div>
        
        <div class="dropzone" id="dropzone">
            <div class="dropzone-icon">📁</div>
            <div class="dropzone-text">
                Drag & drop file here or <strong>click to browse</strong>
            </div>
            <div id="filename" style="margin-top: 1rem; color: #00d4ff;"></div>
            <input type="file" id="fileInput" style="display: none;" 
                   accept="audio/*,image/*,.mp3,.wav,.m4a,.ogg,.flac,.png,.jpg,.jpeg,.bmp,.tiff,.pdf">
        </div>
        
        <div class="options">
            <div class="option" id="modelOption">
                <label>Model Size (bigger = better quality)</label>
                <select id="modelSelect">
                    <option value="tiny">tiny (fastest)</option>
                    <option value="base" selected>base (recommended)</option>
                    <option value="small">small (better)</option>
                    <option value="medium">medium (high quality)</option>
                    <option value="large-v3">large-v3 (best)</option>
                </select>
            </div>
            <div class="option">
                <label>Language</label>
                <select id="langSelect">
                    <option value="">Auto-detect</option>
                    <option value="en" selected>English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="zh">Chinese</option>
                    <option value="ja">Japanese</option>
                    <option value="ko">Korean</option>
                    <option value="ar">Arabic</option>
                    <option value="hi">Hindi</option>
                    <option value="pt">Portuguese</option>
                    <option value="ru">Russian</option>
                </select>
            </div>
        </div>
        
        <button class="btn" id="processBtn" disabled>Process File</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div id="loadingText">Processing...</div>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result" id="result">
            <div class="result-header">
                <div>
                    <div class="result-title">Result</div>
                    <div class="result-meta" id="resultMeta"></div>
                </div>
                <button class="copy-btn" onclick="copyResult()">📋 Copy</button>
            </div>
            <div class="result-text" id="resultText"></div>
        </div>
        
        <div class="footer">
            <p>100% free and open source • <a href="https://github.com">GitHub</a></p>
            <p style="margin-top: 0.5rem;">Powered by <a href="https://github.com/guillaumekln/faster-whisper">faster-whisper</a> & <a href="https://github.com/tesseract-ocr/tesseract">Tesseract</a></p>
        </div>
    </div>
    
    <script>
        let currentMode = 'transcribe';
        let selectedFile = null;
        
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentMode = tab.dataset.mode;
                
                // Update file input accept
                const fileInput = document.getElementById('fileInput');
                if (currentMode === 'transcribe') {
                    fileInput.accept = 'audio/*,.mp3,.wav,.m4a,.ogg,.flac,.wma,.aac,.webm,.opus';
                } else {
                    fileInput.accept = 'image/*,.png,.jpg,.jpeg,.bmp,.tiff,.pdf';
                }
            });
        });
        
        // Drag and drop
        const dropzone = document.getElementById('dropzone');
        
        dropzone.addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
        
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });
        
        dropzone.addEventListener('dragleave', () => {
            dropzone.classList.remove('dragover');
        });
        
        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                selectFile(e.dataTransfer.files[0]);
            }
        });
        
        document.getElementById('fileInput').addEventListener('change', (e) => {
            if (e.target.files.length) {
                selectFile(e.target.files[0]);
            }
        });
        
        function selectFile(file) {
            selectedFile = file;
            document.getElementById('filename').textContent = file.name;
            document.getElementById('processBtn').disabled = false;
        }
        
        // Process button
        document.getElementById('processBtn').addEventListener('click', processFile);
        
        async function processFile() {
            if (!selectedFile) return;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('mode', currentMode);
            formData.append('model', document.getElementById('modelSelect').value);
            formData.append('language', document.getElementById('langSelect').value);
            
            // Show loading
            document.getElementById('loading').classList.add('visible');
            document.getElementById('loadingText').textContent = 
                currentMode === 'transcribe' ? 'Transcribing audio...' : 'Extracting text...';
            document.getElementById('result').classList.remove('visible');
            document.getElementById('error').classList.remove('visible');
            document.getElementById('processBtn').disabled = true;
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Show result
                document.getElementById('resultText').textContent = data.text;
                document.getElementById('resultMeta').textContent = 
                    `${data.duration}s • ${currentMode === 'ocr' ? 'Confidence: ' + data.confidence + '%' : ''}`;
                document.getElementById('result').classList.add('visible');
                
            } catch (err) {
                document.getElementById('error').textContent = err.message;
                document.getElementById('error').classList.add('visible');
            } finally {
                document.getElementById('loading').classList.remove('visible');
                document.getElementById('processBtn').disabled = false;
            }
        }
        
        function copyResult() {
            const text = document.getElementById('resultText').textContent;
            navigator.clipboard.writeText(text);
            const btn = document.querySelector('.copy-btn');
            btn.textContent = '✓ Copied!';
            setTimeout(() => btn.textContent = '📋 Copy', 2000);
        }
    </script>
</body>
</html>
"""


def create_app() -> Flask:
    """Create Flask app for web interface."""
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/process', methods=['POST'])
    def process():
        import time
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        mode = request.form.get('mode', 'transcribe')
        model = request.form.get('model', 'base')
        language = request.form.get('language', '') or None
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, 
                                         suffix=Path(file.filename).suffix) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            start = time.time()
            
            if mode == 'transcribe':
                from .stt import Transcriber
                transcriber = Transcriber(model=model)
                text = transcriber.transcribe_to_text(tmp_path, language=language)
                confidence = None
            else:
                from .ocr import OCR
                # Map language codes for Tesseract
                tesseract_lang = language[:3] if language else 'eng'
                if tesseract_lang == 'eng':
                    tesseract_lang = 'eng'
                engine = OCR(language=tesseract_lang)
                result = engine.extract(tmp_path)
                text = result.text
                confidence = result.confidence
            
            duration = round(time.time() - start, 2)
            
            return jsonify({
                'text': text,
                'duration': duration,
                'confidence': round(confidence, 1) if confidence else None
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
