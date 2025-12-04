# АРХИТЕКТУРА - SberMobile Telegram Bot

## 📐 Общая структура

```
┌─────────────────────────────────────────────────────────────────┐
│                    Telegram User                                 │
│                         (Chat)                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ (Text Message)
┌─────────────────────────────────────────────────────────────────┐
│                  Telegram Bot API                                │
│              (python-telegram-bot v20.5)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │ /start │      │ /help  │      │ Message│
    │ Handler│      │Handler │      │ Handler│
    └────┬───┘      └────┬───┘      └────┬───┘
         │               │              │
         └───────────────┼──────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  FAQ Search Engine     │
            │  (faq_engine.py)       │
            │                        │
            │  • Normalize text      │
            │  • Fuzzy matching      │
            │  • Find best answer    │
            └────────┬───────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼ (Found)                 ▼ (Not Found)
    ┌─────────┐              ┌──────────┐
    │ Answer  │              │ "Not     │
    │ Found   │              │ Found"   │
    │ Response│              │ Message  │
    └────┬────┘              └────┬─────┘
         │                        │
         └────────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │  Log Interaction        │
        │  (database.py)          │
        │                         │
        │  • user_id              │
        │  • message              │
        │  • found (true/false)   │
        │  • category             │
        │  • similarity_score     │
        └────────┬────────────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │    SQLite Database     │
    │    (data/bot.db)       │
    │                        │
    │    Tables:             │
    │    • interactions      │
    │    • users             │
    └────────────────────────┘
```

---

## 📁 Структура файлов

### Каталоги

```
sbermobile-bot/
├── app/                    # Основной пакет приложения
│   ├── __init__.py        # Инициализация пакета
│   ├── bot.py             # Основная логика и инициализация бота
│   ├── handlers.py        # Обработчики команд и сообщений
│   ├── faq_engine.py      # Поиск по FAQ и нормализация текста
│   └── database.py        # Работа с SQLite БД
│
├── data/                   # Данные приложения
│   ├── faq.json           # FAQ база (опционально)
│   └── bot.db             # SQLite база (создается автоматически)
│
├── venv/                   # Виртуальное окружение (не коммитим)
│
├── main.py                # Точка входа приложения
├── requirements.txt       # Зависимости Python
├── .env.example          # Пример переменных окружения
├── .env                  # Актуальные переменные (не коммитим)
├── .gitignore            # Git исключения
├── render.yaml           # Конфиг для Render.com
│
├── README.md             # Полная документация
├── QUICKSTART.md         # Быстрый старт
└── ARCHITECTURE.md       # Этот файл
```

---

## 🔄 Поток обработки сообщения

### 1. Получение сообщения

```
User sends "/start" or text message
          │
          ▼
Application.run_webhook() (in production)
or
Application.run_polling() (in development)
          │
          ▼
Message added to queue
```

### 2. Маршрутизация

```
Message received
          │
          ├─ /start?   → start_command()
          ├─ /help?    → help_command()
          ├─ /contact? → contact_command()
          ├─ /categories? → categories_command()
          └─ Text?     → handle_message()
```

### 3. Обработка обычного сообщения

```
handle_message(user_message)
          │
          ▼
find_answer(user_message)
          │
          ├─ normalize_text(user_message)
          │     └─ lowercase, strip()
          │
          ├─ load_faq()
          │     └─ Load from DEFAULT_FAQ or faq.json
          │
          ├─ For each question in FAQ:
          │     │
          │     ├─ similarity = calculate_similarity(
          │     │                  normalized_user_msg,
          │     │                  normalized_faq_question)
          │     │
          │     └─ Track best_match with highest similarity
          │
          └─ if best_match > THRESHOLD (50%):
               ├─ return {found: True, ...match_data}
               └─ else: return {found: False}
          │
          ▼
if found:
  ├─ format response with answer
  ├─ send to user
  └─ log_interaction(found=True, ...)
else:
  ├─ send "not found" message
  ├─ suggest alternatives
  └─ log_interaction(found=False, ...)
```

### 4. Логирование

```
log_interaction(user_id, message, found, category, score)
          │
          ├─ INSERT INTO interactions (...)
          │
          └─ UPDATE users 
               ├─ last_interaction
               └─ total_queries += 1
```

---

## 🔍 Алгоритм поиска по FAQ

### Метод: Fuzzy String Matching

Используется `difflib.SequenceMatcher` для вычисления схожести строк.

```python
def calculate_similarity(text1, text2):
    # Нормализация
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    
    # Вычисление коэффициента Жаккара
    ratio = SequenceMatcher(None, text1, text2).ratio()
    # ratio: 0 = полностью разные, 1 = идентичные
    
    return ratio
```

### Пример:

```
User: "как подключить есим"
FAQ:  "Как подключить eSIM?"

После нормализации:
User: "как подключить есим"
FAQ:  "как подключить esim?"

Similarity: 85% ✓ (выше 50% threshold)

Result: Ответ найден!
```

### Пример не совпадения:

```
User: "почему не работает интернет"
FAQ:  "Как улучшить качество сигнала?"

Similarity: 35% ✗ (ниже 50% threshold)

Result: Ответ не найден → предложить контакты
```

---

## 📊 Схема БД

### Таблица: interactions

```sql
CREATE TABLE interactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,          -- Telegram user ID
    user_message    TEXT NOT NULL,             -- Исходный вопрос
    found           BOOLEAN NOT NULL,         -- Найден ли ответ (0 или 1)
    category        TEXT,                     -- Категория найденного ответа
    similarity_score REAL,                    -- Коэффициент совпадения (0-1)
    created_at      TIMESTAMP DEFAULT NOW    -- Время запроса
);

-- Индексы для быстрого поиска
CREATE INDEX idx_user_id ON interactions(user_id);
CREATE INDEX idx_created_at ON interactions(created_at);
```

### Таблица: users

```sql
CREATE TABLE users (
    user_id          INTEGER PRIMARY KEY,      -- Telegram user ID
    first_interaction TIMESTAMP DEFAULT NOW,   -- Дата первого контакта
    last_interaction TIMESTAMP DEFAULT NOW,   -- Последний контакт
    total_queries    INTEGER DEFAULT 0        -- Всего вопросов
);
```

### Примеры запросов:

```sql
-- Все вопросы пользователя
SELECT * FROM interactions 
WHERE user_id = 12345 
ORDER BY created_at DESC;

-- Статистика успешности
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN found = 1 THEN 1 ELSE 0 END) as found,
    (SUM(CASE WHEN found = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as success_rate
FROM interactions;

-- Топ категорий
SELECT category, COUNT(*) as count
FROM interactions
WHERE category IS NOT NULL
GROUP BY category
ORDER BY count DESC
LIMIT 10;

-- Активные пользователи (за последние 7 дней)
SELECT user_id, COUNT(*) as queries
FROM interactions
WHERE created_at > datetime('now', '-7 days')
GROUP BY user_id
ORDER BY queries DESC;
```

---

## 🌐 Веб-хуки vs Polling

### Режим Polling (Разработка)

```
┌─────────────────┐
│  Bot Process    │
└────────┬────────┘
         │
         ▼ (Every 1 second)
┌─────────────────────────────────────┐
│  "Hello Telegram, any messages?"    │
│  (getUpdates API call)              │
└────────┬────────────────────────────┘
         │
         ├─ No messages? Wait 1s, retry
         │
         └─ Messages? Process them
```

**Плюсы:**
- Просто для локального тестирования
- Работает за NAT/firewall

**Минусы:**
- Медленнее (задержка 1сек)
- Больше нагрузка на API Telegram
- Не работает хорошо на Render.com бесплатном плане

### Режим Webhooks (Продакшен)

```
┌────────────────────┐
│  Telegram Servers  │
└────────┬───────────┘
         │
         │ (Instant, when message arrives)
         ▼ HTTPS POST
┌─────────────────────────────────┐
│  https://your-service.com/      │
│  webhook/{token}                │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Bot Process (run_webhook())    │
│  • Listens on port 8000         │
│  • Processes update instantly   │
│  • Sends response back          │
└─────────────────────────────────┘
```

**Плюсы:**
- Мгновенная обработка
- Меньше нагрузка на API
- Работает на Render.com бесплатно
- Профессиональный подход

**Минусы:**
- Требует HTTPS
- Требует публичного URL
- Более сложная отладка

**Конфигурация (app/bot.py):**

```python
app.run_webhook(
    listen="0.0.0.0",                    # Слушать на всех интерфейсах
    port=8000,                           # Порт (PORT из .env)
    url_path=f"/webhook/{token}",        # URL путь
    webhook_url=webhook_url              # Полный URL для Telegram
)
```

---

## 🔐 Безопасность

### Проверка переменных окружения

```python
# main.py
required_env_vars = ['TELEGRAM_BOT_TOKEN', 'WEBHOOK_URL']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"Отсутствуют: {missing_vars}")
    sys.exit(1)
```

### Не хранятся в git

```
.gitignore:
.env                  # Не коммитим
.env.local           # Не коммитим
data/bot.db          # Не коммитим БД
venv/                # Не коммитим виртуальное окружение
```

### Токены в Render.com

- Переменные окружения хранятся защищенно в Render.com
- Не видны в исходном коде
- Не видны в GitHub
- Просматриваются только владельцем сервиса

---

## 📈 Масштабируемость

### Текущие ограничения

| Метрика | Значение |
|---------|----------|
| FAQ база | ~35 Q&A (может быть расширена) |
| Пользователей | Неограниченно |
| Сообщений в день | ~10,000 (Render.com free) |
| Размер БД | Неограниченно (SQLite) |
| Время ответа | ~500ms |

### Возможные улучшения для масштаба

1. **Кэширование FAQ**
   ```python
   # Вместо загрузки каждый раз
   FAQ_CACHE = load_faq()  # Один раз при старте
   ```

2. **Асинхронная обработка**
   ```python
   # Использование async/await (уже реализовано)
   async def handle_message(...)
   ```

3. **Миграция БД**
   ```python
   # SQLite → PostgreSQL для большего масштаба
   ```

4. **Redis кэш**
   ```python
   # Для часто задаваемых вопросов
   ```

5. **ML Модели**
   ```python
   # Bert/GPT для лучшего matching
   ```

---

## 🧪 Тестирование

### Локальное тестирование

```bash
# 1. Запустить бота в режиме polling
python main.py --polling

# 2. Открыть Telegram и отправить /start

# 3. Проверить разные команды и вопросы

# 4. Смотреть логи в консоли
```

### Проверка БД

```python
# Интерпретатор Python
from app.database import get_stats
print(get_stats())
```

### Проверка FAQ

```python
from app.faq_engine import find_answer

result = find_answer("как подключить есим")
print(result)
# {
#   'found': True,
#   'category': 'eSIM',
#   'answer': '...',
#   'similarity_score': 0.85
# }
```

---

## 🚀 Развертывание (Render.com)

### Процесс

1. **GitHub** → Push кода
2. **Render.com** → Blueprint читает `render.yaml`
3. **Автоматически:**
   - `pip install -r requirements.txt`
   - `python main.py` (с веб-хуками)
   - Создается публичный URL
4. **Telegram Bot API** → Настраивается webhook на URL
5. **Сообщения** → Текут через webhook

### Мониторинг

```
Render.com Dashboard:
├── Logs (последние события)
├── Environment (переменные)
├── Deploy history (история развертываний)
└── Metrics (CPU, Memory)
```

---

## 📝 Логирование

### Уровни логирования

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Детальная информация")      # DEBUG
logger.info("✅ Процесс завершен")       # INFO
logger.warning("⚠️  Потенциальная проблема")  # WARNING
logger.error("❌ Ошибка произошла")       # ERROR
logger.critical("🚨 Критическая ошибка")   # CRITICAL
```

### Форматирование

```
2025-12-04 14:30:15 - bot - INFO - ✅ Бот успешно запущен!
│                      │          │    │
│                      │          │    └─ Сообщение
│                      │          └─ Уровень (INFO, ERROR, etc)
│                      └─ Модуль (bot, handlers, etc)
└─ Время
```

---

## 🔄 Обновление FAQ

### Способ 1: Отредактировать DEFAULT_FAQ

```python
# app/faq_engine.py
DEFAULT_FAQ = [
    {
        "category": "Новая категория",
        "questions": [
            {
                "question": "Новый вопрос?",
                "answer": "Новый ответ!"
            }
        ]
    }
]
```

### Способ 2: Использовать data/faq.json

```json
[
  {
    "category": "eSIM",
    "questions": [
      {
        "question": "...",
        "answer": "..."
      }
    ]
  }
]
```

---

## 📞 Контакты и поддержка

- **GitHub**: https://github.com/YOUR_USERNAME/sbermobile-bot
- **Render.com**: https://render.com/
- **python-telegram-bot**: https://docs.python-telegram-bot.org/
- **Telegram**: @BotFather

---

**Архитектура обновлена:** 2025-12-04
**Версия:** 1.0.0-beta
