"""
app/handlers.py
Обработчики команд и сообщений
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from app.faq_engine import find_answer, get_categories
from app.database import log_interaction

logger = logging.getLogger(__name__)

# Константы
SUPPORT_PHONE = "☎️ +7 (499) 651-44-44"
SUPPORT_WEBSITE = "https://sbermobile.ru/faq/"
SUPPORT_SHORTCODE = "901"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    
    user = update.effective_user
    logger.info(f"👤 Новый пользователь: {user.username or user.id}")
    
    welcome_message = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🤖 Я <b>SberMobile Support Bot</b> — ваш помощник по вопросам SberMobile\n\n"
        "Я помогу ответить на вопросы о:\n"
        "• 💳 Тарифах и услугах\n"
        "• 🔄 Переносе номера\n"
        "• 📱 eSIM\n"
        "• ⭐ Подписке СберПрайм\n"
        "• 📞 Мобильной связи и интернете\n"
        "• 📋 И многом другом\n\n"
        "<b>Начните с вопроса → я найду ответ! 🔍</b>\n\n"
        "Доступные команды:\n"
        "/help — справка\n"
        "/categories — категории FAQ\n"
        "/contact — контакты поддержки"
    )
    
    await update.message.reply_html(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    
    help_text = (
        "<b>❓ Справка по использованию бота</b>\n\n"
        "<b>Как использовать:</b>\n"
        "1. Напишите свой вопрос об SberMobile\n"
        "2. Бот найдет ответ в базе знаний\n"
        "3. Получите подробный ответ\n\n"
        "<b>Примеры вопросов:</b>\n"
        "• Как подключить eSIM?\n"
        "• Какие тарифы доступны?\n"
        "• Как перенести номер?\n"
        "• Что входит в СберПрайм?\n\n"
        "<b>Если ответ не найден:</b>\n"
        "✉️ Напишите в поддержку\n"
        f"{SUPPORT_PHONE}\n"
        f"Короткий номер: {SUPPORT_SHORTCODE}\n"
        f"🌐 {SUPPORT_WEBSITE}\n\n"
        "<b>Доступные команды:</b>\n"
        "/start — начать заново\n"
        "/categories — показать категории\n"
        "/contact — контакты поддержки"
    )
    
    await update.message.reply_html(help_text)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /contact"""
    
    contact_text = (
        "<b>☎️ Контакты поддержки SberMobile</b>\n\n"
        f"<b>Основной номер:</b>\n{SUPPORT_PHONE}\n\n"
        f"<b>Короткий номер (для номеров СберМобайла):</b>\n{SUPPORT_SHORTCODE}\n\n"
        f"<b>Веб-версия FAQ:</b>\n{SUPPORT_WEBSITE}\n\n"
        "<b>Режим работы:</b>\n24/7\n\n"
        "<b>Время ответа на тикеты:</b>\n⏱️ До 5 дней"
    )
    
    await update.message.reply_html(contact_text)

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /categories"""
    
    categories = get_categories()
    
    categories_text = "<b>📂 Категории FAQ SberMobile</b>\n\n"
    
    for i, category in enumerate(categories, 1):
        categories_text += f"{i}. {category}\n"
    
    categories_text += (
        "\n<i>Спросите что-то из этих категорий, и я найду ответ!</i>\n"
        "Например: \"Как подключить eSIM?\""
    )
    
    await update.message.reply_html(categories_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик обычных сообщений пользователя"""
    
    user_message = update.message.text
    user_id = update.effective_user.id
    
    logger.info(f"💬 Новое сообщение от {user_id}: {user_message[:50]}...")
    
    # Показать индикатор печати
    await update.effective_chat.send_action("typing")
    
    try:
        # Найти ответ в FAQ
        result = find_answer(user_message)
        
        # Логировать взаимодействие
        log_interaction(
            user_id=user_id,
            user_message=user_message,
            found=result['found'],
            category=result.get('category'),
            similarity_score=result.get('similarity_score', 0)
        )
        
        if result['found']:
            # Ответ найден
            response = (
                "✅ <b>Нашел ответ:</b>\n\n"
                f"{result['answer']}\n\n"
                f"<i>Категория: {result['category']}</i>\n"
                f"<i>Релевантность: {result['similarity_score']:.0%}</i>\n\n"
                "Есть еще вопросы? 🤔"
            )
            
            logger.info(f"✅ Ответ найден: {result['category']}")
            
        else:
            # Ответ не найден
            response = (
                "🤔 <b>К сожалению, я не нашел точный ответ на твой вопрос.</b>\n\n"
                "Возможно:\n"
                "1️⃣ Попробуй переформулировать вопрос\n"
                "2️⃣ Используй /categories для просмотра тем\n"
                "3️⃣ Обратись в поддержку\n\n"
                f"☎️ {SUPPORT_PHONE}\n"
                f"📱 {SUPPORT_SHORTCODE} (для номеров СберМобайла)\n\n"
                "Попробуем еще? 🔄"
            )
            
            logger.info(f"❌ Ответ не найден для: {user_message[:30]}")
        
        # Отправить ответ
        await update.message.reply_html(response)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при обработке сообщения: {e}")
        
        error_response = (
            "🚨 <b>Произошла ошибка при обработке вашего запроса.</b>\n\n"
            "Пожалуйста, попробуйте позже или напишите в поддержку:\n"
            f"☎️ {SUPPORT_PHONE}"
        )
        
        await update.message.reply_html(error_response)
