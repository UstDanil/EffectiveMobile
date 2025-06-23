Нужные библиотеки:
pip install redis sqlalchemy pydantic asyncpg fastapi uvicorn pytest pytest-mock pytest-cov httpx

Запуск тестов
pytest -v

Запуск тестов с проверкой покрытия:
pytest --cov-report term-missing --cov=app tests/  

Запуск проекта:
uvicorn app.main:app --reload   

Для наполнения БД:
Запуск скрипта из part_4

Задание:
В продолжение прошлой темы необходимо покрыть собственный проект тестами. 
Необходимо покрыть как низкоуровневые функции, так и end-point’ы FastAPI клиента. 
Будет плюсом, если вы дополнительно реализуете мок функцию.