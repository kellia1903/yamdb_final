![example workflow](https://github.com/kellia1903/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект YaMDb
========================================================
Проект YaMDb собирает отзывы пользователей на произведения
## Технологии
- Python 3.8
- Django
- Django REST Framework
- JWT

## Шаблон наполнения env-файла:
  SECRET_KEY: Секретный ключ проекта. Задается в settings проекта Django.
  DB_ENGINE: Тип базы данных. Используется PostgreSQL.
  DB_NAME: Наименование базы данных.
  POSTGRES_USER: Логин пользователя БД.
  POSTGRES_PASSWORD: Пароль пользователя БД.
  DB_HOST: Название контейнера с БД.
  DB_PORT: Порт используемый БД. По умолчанию 5432.

## Как развернуть и запустить проект у себя? ##
### 1. Склонировать репозиторий в рабочее пространство: ###
```
git clone https://github.com/kellia1903/yamdb_final.git
```
### 2. Затем нужно перейти в папку yamdb_final/infra и создать в ней файл .env с переменными окружения, необходимыми для работы приложения. ###
```
cd yamdb_final/infra
touch .env
```
### 3. Далее следует запустить docker-compose: ###
```
docker-compose up -d --build
```
### 4. При успешном запуске, осуществите миграцию БД: ###
```
docker-compose exec web python manage.py migrate
```
### 5. По завершению миграции, создайте суперпользователя: ###
```
docker-compose exec web python manage.py createsuperuser
```
### 6. После, осуществите сбор файлов статики и медиафайлов внутри контейнера: ###
```
docker-compose exec web python manage.py collectstatic --no-input
```
### 7. Теперь можно наполнить БД тестовыми записями, файл fixtures.json находится в infra_sp2. Выполните команду: ###
```
docker cp fixtures.json <CONTAINER_ID_api_yamdb_web>:/app/
docker-compose exec web python manage.py loaddata fixtures.json
```

## Документация API ##
У проекта есть документация к API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов.

Для её просмотра нужно перейти на эндпоинт `http://127.0.0.1:8000/redoc/`.

## Разработчик ##
  - [Никита Цыбин](https://github.com/kellia1903)
