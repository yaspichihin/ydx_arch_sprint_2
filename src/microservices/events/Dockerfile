FROM python:3.11-slim

# Установим рабочую директорию на уровень с main.py
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаём папку для логов
RUN mkdir -p logs

# Открываем порт
EXPOSE 8082

# Переходим в директорию с main.py
WORKDIR /app

# Запуск приложения через python -m uvicorn для поддержки относительных импортов
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"] 