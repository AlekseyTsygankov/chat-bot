#!/bin/bash

# SberMobile Telegram Bot - Setup Script
# Этот скрипт автоматически создает структуру проекта на Mac

set -e

PROJECT_NAME="sbermobile-bot"
GITHUB_USER=${1:-your-github-username}

echo "🚀 Создание проекта $PROJECT_NAME..."

# 1. Создать директорию проекта
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# 2. Инициализировать git
git init
git config user.email "bot@sbermobile.local"
git config user.name "SberMobile Bot Developer"

# 3. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 4. Установить зависимости
pip install --upgrade pip setuptools wheel

# Файлы будут созданы в следующем шаге
echo "✅ Структура проекта создана!"
echo ""
echo "Следующие шаги:"
echo "1. cd $PROJECT_NAME"
echo "2. source venv/bin/activate"
echo "3. pip install -r requirements.txt"
echo "4. Скопировать файлы конфигурации из ниже"
echo "5. git add . && git commit -m 'Initial commit'"
echo "6. Запушить на GitHub и настроить Render.com"
