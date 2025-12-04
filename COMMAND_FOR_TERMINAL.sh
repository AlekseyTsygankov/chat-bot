#!/bin/bash

###############################################################################
# 🚀 SBERMOBILE TELEGRAM BOT - COMPLETE ONE-LINER FOR MAC
# 
# ✅ ЧТО ЭТА КОМАНДА ДЕЛАЕТ:
# 1. Создает папку проекта sbermobile-bot
# 2. Создает структуру app/ и data/
# 3. Создает виртуальное окружение Python
# 4. Устанавливает все зависимости
# 5. Создает все конфиг-файлы
# 6. Инициализирует Git репозиторий
#
# ✅ ПОСЛЕ ВЫПОЛНЕНИЯ:
# • Все файлы готовы (кроме Python кода - нужно скопировать из документации)
# • Виртуальное окружение активировано
# • Dependencies установлены
# • Git инициализирован
#
# ✅ КОПИРУЙ И ВСТАВЬ ОДНУ ИЗ КОМАНД НИЖЕ В ТЕРМИНАЛ:
###############################################################################

# ВАРИАНТ 1: Самая короткая (копируй от сюда и до следующего комментария)

cd ~ && mkdir sbermobile-bot && cd sbermobile-bot && mkdir -p app data && python3 -m venv venv && source venv/bin/activate && pip install -q python-telegram-bot==20.5 aiohttp==3.9.1 httpx==0.25.1 python-dotenv==1.0.0 pydantic==2.5.0 && touch app/__init__.py && git init && git config user.email "bot@sbermobile.local" && git config user.name "SberMobile Bot" && touch main.py app/bot.py app/handlers.py app/faq_engine.py app/database.py requirements.txt .env.example .gitignore render.yaml README.md && echo "✅ ГОТОВО! Создана структура проекта в $(pwd)"

###############################################################################

# ВАРИАНТ 2: Если вышло не ясно - шаги отдельно:

# Шаг 1: Перейти в home директорию и создать проект
cd ~
mkdir sbermobile-bot
cd sbermobile-bot

# Шаг 2: Создать структуру
mkdir -p app data
touch app/__init__.py

# Шаг 3: Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Шаг 4: Установить зависимости (молча, без вывода)
pip install -q python-telegram-bot==20.5 aiohttp==3.9.1 httpx==0.25.1 python-dotenv==1.0.0 pydantic==2.5.0

# Шаг 5: Инициализировать Git
git init
git config user.email "bot@sbermobile.local"
git config user.name "SberMobile Bot"

# Шаг 6: Создать пустые файлы
touch main.py app/bot.py app/handlers.py app/faq_engine.py app/database.py
touch requirements.txt .env.example .gitignore render.yaml README.md

# Готово!
echo "✅ Структура создана в: $(pwd)"

###############################################################################

# СЛЕДУЮЩИЕ ШАГИ ПОСЛЕ ВЫПОЛНЕНИЯ КОМАНДЫ:

# 1. Откройте папку в VS Code:
#    code .

# 2. Скопируйте содержимое файлов из документации для каждого:
#    - main.py
#    - app/bot.py
#    - app/handlers.py
#    - app/faq_engine.py
#    - app/database.py
#    - requirements.txt
#    - .env.example
#    - .gitignore
#    - render.yaml
#    - README.md

# 3. Создайте .env файл:
#    cp .env.example .env
#    nano .env
#    # Заполнить: TELEGRAM_BOT_TOKEN и WEBHOOK_URL

# 4. Запустите локально:
#    python main.py --polling

# 5. Тестируйте в Telegram!

###############################################################################
