"""
app/bot.py
Основной модуль с логикой бота
Поддерживает polling и webhook режимы
"""

import os
import logging
from telegram import Update, BotCommand
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters,
    ContextTypes,
)

from app.handlers import (
    start_command,
    help_command,
    contact_command,
    categories_command,
    handle_message
)
from app.database import init_database, close_database

logger = logging.getLogger(__name__)

def create_bot_polling():
    """
    Создать и запустить бота в режиме POLLING (бесплатный)
    Бот сам спрашивает Telegram API о новых сообщениях каждую секунду
    """
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен!")
    
    # Инициализировать базу данных
    init_database()
    logger.info("📊 База данных инициализирована")
    
    # Создать приложение
    app = Application.builder().token(token).build()
    
    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("categories", categories_command))
    
    # Обработчик для обычных сообщений (должен быть в конце!)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработка ошибок
    app.add_error_handler(error_handler)
    
    # Установить команды бота
    logger.info("⚙️  Регистрация команд бота...")
    
    # Запустить бота в режиме POLLING
    logger.info("🔄 Запуск в режиме POLLING (Render Free Tier)")
    logger.info("⏱️  Проверка сообщений каждую секунду...")
    
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        close_loop_on_stop=True
    )

def create_bot_webhook(port: int = 8000, webhook_url: str = None):
    """
    Создать и запустить бота с WEBHOOK (платный)
    Telegram сам отправляет сообщения боту через HTTP
    
    Args:
        port: Порт для веб-сервера
        webhook_url: URL для веб-хука (например, https://example.com/webhook)
    """
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен!")
    
    if not webhook_url:
        raise ValueError("WEBHOOK_URL не установлен!")
    
    # Инициализировать базу данных
    init_database()
    logger.info("📊 База данных инициализирована")
    
    # Создать приложение
    app = Application.builder().token(token).build()
    
    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("categories", categories_command))
    
    # Обработчик для обычных сообщений (должен быть в конце!)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработка ошибок
    app.add_error_handler(error_handler)
    
    # Установить команды бота
    logger.info("⚙️  Регистрация команд бота...")
    
    # Настроить веб-хуки
    logger.info(f"🔗 Настройка веб-хука: {webhook_url}")
    
    # Запустить бота с веб-хуками
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=f"/webhook/{token}",
        webhook_url=webhook_url
    )
    
    return app

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logger.error(f"❌ Ошибка: {context.error}", exc_info=context.error)
    
    if update and update.effective_chat:
        try:
            await update.effective_chat.send_message(
                "🚨 Произошла ошибка. Попробуйте позже или напишите в поддержку.\n"
                "☎️ +7 (499) 651-44-44"
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение об ошибке: {e}")
