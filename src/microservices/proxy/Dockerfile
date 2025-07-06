FROM python:3.11-slim

WORKDIR /app

# Установим зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаём папку для логов
RUN mkdir -p logs

# Открываем порт
EXPOSE 8000

# Запуск приложения через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 