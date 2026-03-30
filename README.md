# Whisper Transcription Server

HTTP сервер для транскрипции аудио через Groq Whisper API (Deepgram-compatible endpoint).

## Возможности

- 🎤 Транскрибирует голосовые сообщения в текст
- 🔌 Deepgram-compatible API (endpoint `/v1/listen`)
- 🚀 Groq Whisper-large-v3-turbo (быстро и точно)
- 🌍 Авто-определение языка
- 💾 Не хранит аудио-файлы

## Установка

```bash
pip install groq
```

## Конфигурация

Переменные окружения:
```bash
GROQ_API_KEY=your_groq_api_key
```

Получить ключ: https://console.groq.com/keys

## Запуск

```bash
python3 whisper-server.py
```

Сервер слушает на `http://127.0.0.1:9876`

## API

### POST /v1/listen

```bash
curl -X POST http://127.0.0.1:9876/v1/listen \
  -F "audio=@voice.ogg"
```

Ответ (JSON):
```json
{
  "results": {
    "channels": [{
      "alternatives": [{
        "transcript": "Привет, как дела?"
      }]
    }]
  }
}
```

## Systemd Service

```ini
[Unit]
Description=Whisper Transcription Server
After=network.target

[Service]
Type=simple
User=clawd
WorkingDirectory=/home/clawd/whisper-server
Environment="GROQ_API_KEY=your_key"
ExecStart=/usr/bin/python3 /home/clawd/whisper-server/whisper-server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Интеграция с OpenClaw

В OpenClaw config установите:
```json
{
  "transcription": {
    "provider": "deepgram",
    "endpoint": "http://127.0.0.1:9876"
  }
}
```

## Модель

- **whisper-large-v3-turbo** — баланс скорости и точности
- Поддержка 90+ языков
- Автоопределение языка

## Лицензия

MIT
