#!/usr/bin/env python3
"""
Whisper transcription server (Deepgram mock) using Groq API via curl.
"""

import os, json, tempfile, logging, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger("whisper-server")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL   = os.environ.get("GROQ_MODEL", "whisper-large-v3-turbo")
GROQ_URL     = "https://api.groq.com/openai/v1/audio/transcriptions"


def transcribe_groq(audio_data: bytes) -> tuple[str, str]:
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name
    try:
        result = subprocess.run([
            "curl", "-s", "-X", "POST", GROQ_URL,
            "-H", f"Authorization: Bearer {GROQ_API_KEY}",
            "-F", f"file=@{tmp_path};type=audio/ogg",
            "-F", f"model={GROQ_MODEL}",
            "-F", "response_format=verbose_json",
        ], capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        if "error" in data:
            raise Exception(data["error"])
        return data.get("text", "").strip(), data.get("language", "unknown")
    finally:
        os.unlink(tmp_path)


class DeepgramMockHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): log.info(fmt % args)

    def do_POST(self):
        if not self.path.startswith("/v1/listen"):
            self.send_response(404); self.end_headers(); return

        length = int(self.headers.get("Content-Length", 0))
        audio  = self.rfile.read(length)
        if not audio:
            self._error(400, "No audio data"); return

        try:
            transcript, lang = transcribe_groq(audio)
            log.info(f"Groq [{lang}]: {transcript[:100]}")
        except Exception as e:
            log.error(f"Error: {e}"); self._error(500, str(e)); return

        resp = {"results": {"channels": [{"alternatives": [
            {"transcript": transcript, "confidence": 0.99, "words": []}
        ]}]}, "metadata": {"model": GROQ_MODEL, "detected_language": lang}}
        body = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code, msg):
        body = json.dumps({"error": msg}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    if not GROQ_API_KEY:
        log.error("GROQ_API_KEY not set!"); exit(1)
    port = int(os.environ.get("WHISPER_PORT", "9876"))
    log.info(f"Groq Whisper server 127.0.0.1:{port} model={GROQ_MODEL}")
    HTTPServer(("127.0.0.1", port), DeepgramMockHandler).serve_forever()
