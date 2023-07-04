![example event parameter](https://github.com/VasilievVv/foodgram-project-react/actions/workflows/diplom_workflow.yml/badge.svg?event=push)

# Сайт Foodgram, «Продуктовый помощник».

## Описание

Дипломный проект по реализации API для онлайн-сервиса.
На этом сервисе пользователи могут:

- публиковать рецепты;
- подписываться на публикации других пользователей;
- добавлять понравившиеся рецепты в список «Избранное»;
- перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд;

Проект упакован в Docker.

Образ на DockerHub: vyacheslavv/diplom:latest

server http://130.193.49.244/

Юзер - alex - username
email - admin@admin.admin
Пароль - из сообщения в ревью

## Шаблон заполнения .env файла


DB_ENGINE=*<тип БД>*

DB_NAME=*<имя базы данных>*

POSTGRES_USER=*<логин для подключения к базе данных>*

POSTGRES_PASSWORD=*<пароль для подключения к БД>*

DB_HOST=*<название контейнера>*

DB_PORT=*<порт для подключения к БД>*

## Запуск приложения в контейнерах

Клонировать репозиторий и перейти в папку infra в командной строке:
```
git clone https://github.com/VasilievVv/foodgram-project-react.git
```

```
cd infra
```

Запустить сборку контейнеров docker-compose:

```
docker-compose up -d --build
```

Загрузка ингредиентов в БД:

```
docker-compose exec web python manage.py load_ingredient_csv
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

## Стек используемых технологий

django, django rest framework, docker, docker-compose, postgresql, nginx, docke hub,
github actions, yandex.cloud

## Об авторе

Васильев Вячеслав - студент Яндекс Практикум факультет back-end разработки