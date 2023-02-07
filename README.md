![example workflow](https://github.com/kellia1903/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

Проект YaMDb
========================================================
Проект YaMDb собирает отзывы пользователей на произведения

Функционал проекта адаптирован для использования PostgreSQL и развертывания в контейнерах Docker. Используются инструменты CI и CD.

## Технологии
 - Python 3.7
 - Django 2.2.16
 - REST Framework 3.12.4
 - PyJWT 2.1.0
 - Django filter 21.1
 - Gunicorn 20.0.4
 - PostgreSQL 12.2
 - Docker 20.10.2
 - подробнее см. прилагаемый файл зависимостей requrements.txt

## Шаблон наполнения env-файла:
```
  SECRET_KEY: Секретный ключ проекта. Задается в settings проекта Django.
  DB_ENGINE: Тип базы данных. Используется PostgreSQL.
  DB_NAME: Наименование базы данных.
  POSTGRES_USER: Логин пользователя БД.
  POSTGRES_PASSWORD: Пароль пользователя БД.
  DB_HOST: Название контейнера с БД.
  DB_PORT: Порт используемый БД. По умолчанию 5432.
```
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
### 7. Теперь можно наполнить БД тестовыми записями, файл fixtures.json находится в infra. Выполните команду: ###
```
docker cp fixtures.json <CONTAINER_ID_api_yamdb_web>:/app/
docker-compose exec web python manage.py loaddata fixtures.json
```

## Документация API ##
У проекта есть документация к API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов.

Для её просмотра нужно перейти на эндпоинт `http://127.0.0.1:8000/redoc/`.

## Проект доступен по ссылке ##

  http://158.160.5.172

## Разработчик ##
  - [Никита Цыбин](https://github.com/kellia1903)
