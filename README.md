# URL_shortener
Мини-сервис, который позволяет сокращать длинные URL и отслеживать клики по ним.
Особенности:
- Генерация коротких ссылок
- Сохранение оригинального URL
- Счетчик кликов по каждой ссылке
- Сбор простой аналитики (дата клика, IP, User-Agent)

## Стек технологий
- Python 3.11+
- FastAPI (REST API)
- SQLAlchemy + SQLite (или PostgreSQL)
- Uvicorn (для запуска сервера)
- Pydantic (валидация данных)

---

## Установка

Клонируем репозиторий:
```
git clone https://github.com/veb-bet/URL_shortener.git
cd url-shortener
```

Создаем виртуальное окружение и активируем его:
```
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

Устанавливаем зависимости:
```
pip install -r requirements.txt
```

Запускаем сервер:
```
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу http://127.0.0.1:8000.

---

## API Endpoints
### 1. Создание короткой ссылки

POST /shorten

Request:
```
{
  "url": "https://example.com/some/very/long/url"
}
```

Response:
```
{
  "short_url": "http://127.0.0.1:8000/abc123",
  "original_url": "https://example.com/some/very/long/url"
}
```
### 2. Редирект по короткой ссылке

GET /{short_id}

Пример: http://127.0.0.1:8000/abc123

Перенаправляет на оригинальный URL

Увеличивает счетчик кликов

Сохраняет IP и User-Agent

### 3. Получение аналитики

GET /analytics/{short_id}

Response:
```
{
  "original_url": "https://example.com/some/very/long/url",
  "short_url": "http://127.0.0.1:8000/abc123",
  "clicks": 12,
  "click_details": [
    {
      "timestamp": "2025-09-26T12:34:56",
      "ip": "127.0.0.1",
      "user_agent": "Mozilla/5.0 ..."
    }
  ]
}
```
