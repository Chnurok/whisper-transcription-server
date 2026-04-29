# Whisper Transcription Server

A tiny self-hosted HTTP server that accepts audio and returns a **Deepgram-compatible** transcription response backed by the **Groq Whisper API**.

This project is meant for the practical case where an existing tool already expects a Deepgram-style endpoint, but you want a lightweight local bridge instead of rewriting that integration.

## What it does

- accepts uploaded audio on `POST /v1/listen`
- sends transcription requests to the Groq Whisper API
- returns a compact Deepgram-like JSON response
- includes detected language metadata
- runs as a single small Python process
- binds to `127.0.0.1` by default for private/local use

## Why this exists

A lot of automations and voice tools are already wired to speak one API format. This server acts as a compatibility layer so those tools can keep working while using Groq for speech-to-text.

## Requirements

- Python 3.10+
- `curl`
- a Groq API key

## Install

```bash
git clone https://github.com/Chnurok/whisper-transcription-server.git
cd whisper-transcription-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

```bash
export GROQ_API_KEY=your_groq_api_key
export GROQ_MODEL=whisper-large-v3-turbo
export WHISPER_PORT=9876
```

Groq keys: <https://console.groq.com/keys>

## Run

```bash
python3 whisper-server.py
```

Default address:

```text
http://127.0.0.1:9876
```

## API

### `POST /v1/listen`

Example:

```bash
curl -X POST http://127.0.0.1:9876/v1/listen \
  -F "audio=@voice.ogg"
```

Example response:

```json
{
  "results": {
    "channels": [
      {
        "alternatives": [
          {
            "transcript": "Привет, как дела?",
            "confidence": 0.99,
            "words": []
          }
        ]
      }
    ]
  },
  "metadata": {
    "model": "whisper-large-v3-turbo",
    "detected_language": "ru"
  }
}
```

## Good fit for

- local assistant tooling
- Telegram or voice-note workflows
- automation pipelines that already expect a Deepgram-like response
- quick internal deployments on a VPS or home server

## Notes

- This is intentionally small and easy to inspect.
- The server currently handles audio by writing it to a temporary file and sending it through `curl`.
- It is best suited to personal tools, internal services, and lightweight deployments.

## License

MIT
