FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

# Копирование файлов проекта в контейнер
COPY dogs_api/requirements.txt /app/requirements.txt
COPY ./.env /app/.env

# Установка зависимостей Python
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY dogs_api/app /app

ENV PYTHONPATH "/app"

COPY dogs_api/script.sh /app/script.sh
RUN chmod +x /app/script.sh
CMD [ "sh", "-c", "/app/script.sh" ]