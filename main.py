"""
SberMobile Support Bot for Telegram
Главный модуль приложения
Поддерживает режимы: polling (бесплатный) и webhooks (платный)
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Проверка токена
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    logger.error("❌ Отсутствует переменная окружения: TELEGRAM_BOT_TOKEN")
    sys.exit(1)

def main():
    """Запуск приложения"""
    from app.bot import create_bot_polling, create_bot_webhook
    
    # Парсер аргументов
    parser = argparse.ArgumentParser(description='SberMobile Telegram Bot')
    parser.add_argument('--polling', action='store_true', help='Использовать polling режим (бесплатный)')
    parser.add_argument('--webhook', action='store_true', help='Использовать webhook режим (требует платный Render)')
    args = parser.parse_args()
    
    logger.info("🚀 Запуск SberMobile Support Bot...")
    
    # Определить режим
    if args.polling:
        logger.info("📡 Режим: POLLING (бесплатный, Render Free Tier)")
        logger.info("⏱️  Задержка: ~1 сек между проверками")
        create_bot_polling()
        
    elif args.webhook:
        logger.info("📡 Режим: WEBHOOK (веб-хуки, требует платный Render)")
        webhook_url = os.getenv('WEBHOOK_URL')
        if not webhook_url:
            logger.error("❌ Отсутствует WEBHOOK_URL для режима webhooks")
            sys.exit(1)
        port = int(os.getenv('PORT', 8000))
        logger.info(f"🔌 Порт: {port}")
        logger.info(f"🔗 Webhook URL: {webhook_url}")
        create_bot_webhook(port=port, webhook_url=webhook_url)
        
    else:
        # По умолчанию polling (для Render Free Tier)
        logger.info("📡 Режим: POLLING (по умолчанию)")
        logger.info("ℹ️  Используй флаг --webhook для режима webhooks")
        create_bot_polling()
    
    logger.info("✅ Бот успешно запущен!")
    logger.info("💬 Бот готов к приему сообщений")

if __name__ == '__main__':
    main()
