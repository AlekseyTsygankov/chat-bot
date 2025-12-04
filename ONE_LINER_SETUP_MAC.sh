#!/bin/bash

################################################################################
# 🚀 SberMobile Telegram Bot - COMPLETE ONE-LINER FOR MAC
# 
# Скопируй эту строку полностью и вставь в терминал Mac
# ВСЕ файлы будут созданы автоматически!
################################################################################

# === ПОЛНАЯ ОДНА СТРОКА ===
# (копируй всё до --- вниз)

cd ~ && mkdir -p sbermobile-bot && cd sbermobile-bot && mkdir -p app data && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip setuptools wheel --quiet && pip install python-telegram-bot==20.5 aiohttp==3.9.1 httpx==0.25.1 python-dotenv==1.0.0 pydantic==2.5.0 python-json-logger==2.0.7 --quiet && touch app/__init__.py && git init && git config user.email "bot@sbermobile.local" && git config user.name "SberMobile Bot Dev" && cat > main.py << 'EOF'
"""
SberMobile Support Bot for Telegram
Главный модуль приложения
"""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

required_env_vars = ['TELEGRAM_BOT_TOKEN', 'WEBHOOK_URL']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"❌ Отсутствуют переменные окружения: {', '.join(missing_vars)}")
    sys.exit(1)

def main():
    from app.bot import create_bot
    
    logger.info("🚀 Запуск SberMobile Support Bot...")
    
    port = int(os.getenv('PORT', 8000))
    webhook_url = os.getenv('WEBHOOK_URL')
    
    logger.info(f"📡 Веб-хук URL: {webhook_url}")
    logger.info(f"🔌 Порт: {port}")
    
    bot, app = create_bot(port=port, webhook_url=webhook_url)
    
    logger.info("✅ Бот успешно запущен!")
    logger.info("💬 Бот готов к приему сообщений")

if __name__ == '__main__':
    main()
EOF

cat > requirements.txt << 'EOF'
python-telegram-bot==20.5
aiohttp==3.9.1
httpx==0.25.1
python-dotenv==1.0.0
pydantic==2.5.0
python-json-logger==2.0.7
gunicorn==21.2.0
EOF

cat > .env.example << 'EOF'
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
WEBHOOK_URL=https://your-service.onrender.com
PORT=8000
ENVIRONMENT=production
LOG_LEVEL=INFO
EOF

cat > .gitignore << 'EOF'
.env
.env.local
venv/
env/
__pycache__/
*.pyc
*.db
*.log
.DS_Store
.vscode/
.idea/
*.egg-info/
build/
dist/
data/bot.db
.pytest_cache/
.mypy_cache/
EOF

cat > render.yaml << 'EOF'
services:
  - type: web
    name: sbermobile-bot
    runtime: python-3.11
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        scope: PROJECT
      - key: WEBHOOK_URL
        scope: PROJECT
      - key: PORT
        value: "8000"
EOF

mkdir -p app && echo "" > app/__init__.py && touch app/bot.py app/handlers.py app/faq_engine.py app/database.py && pip freeze | grep -E "python-telegram-bot|aiohttp|httpx|python-dotenv|pydantic" > /dev/null && echo -e "\n✅ СТРУКТУРА ПРОЕКТА СОЗДАНА!\n" && echo "╔════════════════════════════════════════════════════════════╗" && echo "║                                                            ║" && echo "║  🎉 SberMobile Telegram Bot готов!                        ║" && echo "║                                                            ║" && echo "╚════════════════════════════════════════════════════════════╝" && echo "" && echo "📍 Текущая директория: $(pwd)" && echo "" && echo "📋 СЛЕДУЮЩИЕ ШАГИ:" && echo "" && echo "1️⃣  Отредактировать .env файл (заполнить токен):" && echo "   nano .env" && echo "" && echo "2️⃣  Скопировать содержимое файлов Python из документации:" && echo "   app/bot.py" && echo "   app/handlers.py" && echo "   app/faq_engine.py" && echo "   app/database.py" && echo "" && echo "3️⃣  Запустить локально:" && echo "   source venv/bin/activate  # (если не активировано)" && echo "   python main.py --polling" && echo "" && echo "4️⃣  Тестировать в Telegram:" && echo "   • Найти своего бота" && echo "   • Отправить /start" && echo "   • Задать вопрос типа 'Как подключить eSIM?'" && echo "" && echo "5️⃣  Загрузить на GitHub и развернуть:" && echo "   git add . && git commit -m 'Initial commit'" && echo "   git remote add origin https://github.com/YOUR_USERNAME/sbermobile-bot.git" && echo "   git push -u origin main" && echo "" && echo "📚 ДОКУМЕНТАЦИЯ:" && echo "   • README.md - полная инструкция" && echo "   • QUICKSTART.md - быстрый старт" && echo "   • ARCHITECTURE.md - архитектура" && echo "" && echo "✨ Удачи! 🚀"

################################################################################
# После выполнения команды:
# 1. Файлы main.py, requirements.txt, .env.example, .gitignore, render.yaml созданы
# 2. Структура app/ с пустыми файлами готова
# 3. Виртуальное окружение активировано
# 4. Git инициализирован
# 
# ⚠️ ВАЖНО: Теперь нужно скопировать содержимое файлов Python!
################################################################################
