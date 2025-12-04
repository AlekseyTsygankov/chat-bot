# Используем официальный Python образ
FROM python:3.11-slim

# Установить рабочую директорию
WORKDIR /app

# Копировать requirements.txt
COPY requirements.txt .

# Установить зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копировать весь код приложения
COPY . .

# Запустить бота в режиме POLLING (для Render FREE TIER)
CMD ["python", "main.py", "--polling"]
