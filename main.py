"""
SberMobile Support Bot for Telegram
Главный модуль приложения
"""

import os
import sys
import logging
from pathlib import Path

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Проверка необходимых переменных окружения
required_env_vars = ['TELEGRAM_BOT_TOKEN', 'WEBHOOK_URL']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"❌ Отсутствуют переменные окружения: {', '.join(missing_vars)}")
    sys.exit(1)

def main():
    """Запуск приложения"""
    from app.bot import create_bot
    
    logger.info("🚀 Запуск SberMobile Support Bot...")
    
    # Получить порт из переменной окружения (Render.com использует переменную PORT)
    port = int(os.getenv('PORT', 8000))
    webhook_url = os.getenv('WEBHOOK_URL')
    
    logger.info(f"📡 Веб-хук URL: {webhook_url}")
    logger.info(f"🔌 Порт: {port}")
    
    # Создать и запустить бота
    bot, app = create_bot(port=port, webhook_url=webhook_url)
    
    logger.info("✅ Бот успешно запущен!")
    logger.info("💬 Бот готов к приему сообщений")

if __name__ == '__main__':
    main()
