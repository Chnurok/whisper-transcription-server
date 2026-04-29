# Whisper Transcription Server

A tiny self-hosted HTTP server that accepts audio and returns a **Deepgram-compatible** transcription response backed by the **Groq Whisper API**.

This is useful when you want a lightweight local bridge for tools that already speak the Deepgram format, but you want to run transcription through Groq instead.

## Features

- 🎤 Accepts uploaded audio and returns plain text transcription
- 🔌 Deepgram-like endpoint: `POST /v1/listen`
- 🚀 Uses `whisper-large-v3-turbo` by default
- 🌍 Returns detected language metadata
- 🪶 Very small deployment footprint
- 🏠 Binds to `127.0.0.1` by default for local/private use

## Requirements

- Python 3.10+
- `curl` available on the host
- A Groq API key

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Environment variables:

```bash
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=whisper-large-v3-turbo
WHISPER_PORT=9876
```

Get an API key here: <https://console.groq.com/keys>

## Run locally

```bash
python3 whisper-server.py
```

Server address:

```text
http://127.0.0.1:9876
```

## API

### POST `/v1/listen`

Example request:

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

### Notes about compatibility

The response shape is intentionally close to Deepgram for easier drop-in integration, but this project is a lightweight adapter rather than a full Deepgram implementation.

## OpenClaw integration

Use a Deepgram-style transcription endpoint in your OpenClaw config:

```json
{
  "transcription": {
    "provider": "deepgram",
    "endpoint": "http://127.0.0.1:9876"
  }
}
```

## Systemd example

```ini
[Unit]
Description=Whisper Transcription Server
After=network.target

[Service]
Type=simple
User=clawd
WorkingDirectory=/home/clawd/whisper-server
Environment="GROQ_API_KEY=your_key"
Environment="GROQ_MODEL=whisper-large-v3-turbo"
Environment="WHISPER_PORT=9876"
ExecStart=/usr/bin/python3 /home/clawd/whisper-server/whisper-server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Limitations

- Expects audio to be posted as request body/form data in a simple local workflow
- Uses `curl` under the hood instead of a dedicated Python SDK flow
- Not intended as a hardened public internet service without a reverse proxy / auth layer

## License

MIT
