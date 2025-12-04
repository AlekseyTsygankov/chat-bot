#!/bin/bash

################################################################################
# SberMobile Telegram Bot - Auto Setup Script для Mac
# Этот скрипт полностью автоматизирует создание проекта на Mac
#
# Использование:
#   bash <(curl -s https://your-script-url.sh)
# ИЛИ локально:
#   bash setup_project.sh
################################################################################

set -e  # Выйти при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для вывода
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка необходимых команд
check_requirements() {
    print_header "Проверка требований"
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 не установлен"
        echo "Установите Python3: brew install python3"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "Git не установлен"
        echo "Установите Git: brew install git"
        exit 1
    fi
    
    print_success "Python3: $(python3 --version)"
    print_success "Git: $(git --version)"
}

# Создание структуры проекта
create_project_structure() {
    print_header "Создание структуры проекта"
    
    PROJECT_NAME="sbermobile-bot"
    
    if [ -d "$PROJECT_NAME" ]; then
        print_warning "Директория $PROJECT_NAME уже существует"
        read -p "Хотите удалить и создать заново? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$PROJECT_NAME"
            print_info "Директория удалена"
        else
            print_error "Отмена операции"
            exit 1
        fi
    fi
    
    # Создать основные директории
    mkdir -p "$PROJECT_NAME/app"
    mkdir -p "$PROJECT_NAME/data"
    
    cd "$PROJECT_NAME"
    print_success "Структура создана в: $(pwd)"
}

# Инициализировать Git репозиторий
init_git() {
    print_header "Инициализация Git"
    
    git init
    git config user.email "bot@sbermobile.local"
    git config user.name "SberMobile Bot Developer"
    
    print_success "Git репозиторий инициализирован"
}

# Создать виртуальное окружение
create_venv() {
    print_header "Создание виртуального окружения"
    
    python3 -m venv venv
    source venv/bin/activate
    
    print_success "Виртуальное окружение создано"
    print_info "Активировано: $(which python)"
}

# Создание файлов проекта
create_files() {
    print_header "Создание файлов проекта"
    
    # app/__init__.py
    touch app/__init__.py
    print_info "Создан: app/__init__.py"
    
    # Остальные файлы будут скопированы из файловой системы
    print_info "Файлы Python будут добавлены в следующем шаге"
}

# Установка зависимостей
install_dependencies() {
    print_header "Установка зависимостей"
    
    pip install --upgrade pip setuptools wheel
    
    # Основные зависимости
    print_info "Установка python-telegram-bot..."
    pip install python-telegram-bot==20.5
    
    print_info "Установка остальных пакетов..."
    pip install \
        aiohttp==3.9.1 \
        httpx==0.25.1 \
        python-dotenv==1.0.0 \
        pydantic==2.5.0 \
        python-json-logger==2.0.7
    
    print_success "Все зависимости установлены"
}

# Создание requirements.txt
create_requirements() {
    print_header "Создание requirements.txt"
    
    pip freeze > requirements.txt
    print_success "requirements.txt создан"
}

# Инструкции для завершения
print_final_instructions() {
    print_header "✅ ПРОЕКТ УСПЕШНО СОЗДАН!"
    
    echo ""
    echo -e "${GREEN}Следующие шаги:${NC}"
    echo ""
    echo "1️⃣  Перейти в директорию:"
    echo -e "   ${YELLOW}cd sbermobile-bot${NC}"
    echo ""
    echo "2️⃣  Активировать виртуальное окружение:"
    echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    echo ""
    echo "3️⃣  Скопировать файлы Python (используй код из документации):"
    echo -e "   ${YELLOW}app/bot.py${NC}"
    echo -e "   ${YELLOW}app/handlers.py${NC}"
    echo -e "   ${YELLOW}app/faq_engine.py${NC}"
    echo -e "   ${YELLOW}app/database.py${NC}"
    echo -e "   ${YELLOW}main.py${NC}"
    echo ""
    echo "4️⃣  Скопировать конфиг-файлы:"
    echo -e "   ${YELLOW}.env.example${NC}"
    echo -e "   ${YELLOW}.gitignore${NC}"
    echo -e "   ${YELLOW}render.yaml${NC}"
    echo -e "   ${YELLOW}README.md${NC}"
    echo ""
    echo "5️⃣  Создать .env файл:"
    echo -e "   ${YELLOW}cp .env.example .env${NC}"
    echo -e "   ${YELLOW}nano .env${NC}"
    echo "   Заполнить: TELEGRAM_BOT_TOKEN и WEBHOOK_URL"
    echo ""
    echo "6️⃣  Инициализировать Git:"
    echo -e "   ${YELLOW}git add .${NC}"
    echo -e "   ${YELLOW}git commit -m 'Initial commit: SberMobile Bot'${NC}"
    echo ""
    echo "7️⃣  Создать репозиторий на GitHub:"
    echo -e "   ${YELLOW}https://github.com/new${NC}"
    echo ""
    echo "8️⃣  Добавить remote и запушить:"
    echo -e "   ${YELLOW}git remote add origin https://github.com/YOUR_USERNAME/sbermobile-bot.git${NC}"
    echo -e "   ${YELLOW}git branch -M main${NC}"
    echo -e "   ${YELLOW}git push -u origin main${NC}"
    echo ""
    echo "9️⃣  Развернуть на Render.com:"
    echo -e "   ${YELLOW}https://render.com${NC}"
    echo "   • New → Blueprint"
    echo "   • Выбрать GitHub репозиторий"
    echo "   • Render.com прочитает render.yaml"
    echo "   • Заполнить переменные окружения"
    echo "   • Deploy!"
    echo ""
    echo -e "${BLUE}📚 Полная документация в README.md${NC}"
    echo ""
}

# Главная функция
main() {
    print_header "🚀 SberMobile Telegram Bot - Setup для Mac"
    echo ""
    
    check_requirements
    create_project_structure
    init_git
    create_venv
    create_files
    install_dependencies
    create_requirements
    print_final_instructions
}

# Запуск
main
