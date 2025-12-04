"""
app/database.py
Работа с базой данных
"""

import os
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / "data" / "bot.db"

def get_db_connection():
    """Получить соединение с БД"""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Инициализировать базу данных"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Таблица взаимодействий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_message TEXT NOT NULL,
        found BOOLEAN NOT NULL,
        category TEXT,
        similarity_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_queries INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()
    
    logger.info("✅ База данных инициализирована")

def log_interaction(user_id: int, user_message: str, found: bool, category: str = None, similarity_score: float = 0):
    """Логировать взаимодействие пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Добавить взаимодействие
        cursor.execute('''
        INSERT INTO interactions (user_id, user_message, found, category, similarity_score)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, user_message, found, category, similarity_score))
        
        # Обновить информацию о пользователе
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id) VALUES (?)
        ''', (user_id,))
        
        cursor.execute('''
        UPDATE users 
        SET last_interaction = CURRENT_TIMESTAMP, total_queries = total_queries + 1
        WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Взаимодействие залогировано для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при логировании: {e}")

def get_user_stats(user_id: int) -> dict:
    """Получить статистику пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM users WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'user_id': row['user_id'],
                'first_interaction': row['first_interaction'],
                'last_interaction': row['last_interaction'],
                'total_queries': row['total_queries']
            }
        return None
        
    except Exception as e:
        logger.error(f"❌ Ошибка при получении статистики: {e}")
        return None

def get_stats() -> dict:
    """Получить общую статистику"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Общее количество запросов
        cursor.execute('SELECT COUNT(*) as total FROM interactions')
        total_queries = cursor.fetchone()['total']
        
        # Количество успешных ответов
        cursor.execute('SELECT COUNT(*) as found FROM interactions WHERE found = 1')
        found_answers = cursor.fetchone()['found']
        
        # Количество уникальных пользователей
        cursor.execute('SELECT COUNT(DISTINCT user_id) as users FROM users')
        unique_users = cursor.fetchone()['users']
        
        # Процент успешности
        success_rate = (found_answers / total_queries * 100) if total_queries > 0 else 0
        
        # Топ вопросов
        cursor.execute('''
        SELECT user_message, COUNT(*) as count 
        FROM interactions 
        GROUP BY user_message 
        ORDER BY count DESC 
        LIMIT 10
        ''')
        top_questions = [{'question': row['user_message'], 'count': row['count']} for row in cursor.fetchall()]
        
        # Топ категорий
        cursor.execute('''
        SELECT category, COUNT(*) as count 
        FROM interactions 
        WHERE category IS NOT NULL
        GROUP BY category 
        ORDER BY count DESC 
        LIMIT 10
        ''')
        top_categories = [{'category': row['category'], 'count': row['count']} for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total_queries': total_queries,
            'found_answers': found_answers,
            'unique_users': unique_users,
            'success_rate': success_rate,
            'top_questions': top_questions,
            'top_categories': top_categories
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка при получении статистики: {e}")
        return {}

def close_database():
    """Закрыть БД (вызывается при остановке приложения)"""
    logger.info("📊 База данных закрыта")
