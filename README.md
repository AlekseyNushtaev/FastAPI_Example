# Описание веб-приложения

Веб-приложение представляет собой API форума. Авторизованные пользователи могут создавать посты и комменты под постами.

# Инструкция по запуску

Выполните команду в корневой директории проекта для запуска docker-compose\
*docker-compose up -d*

Далее выполняйте http-запросы для работы в веб-приложении\
[Документация по эндпоинтам (активна при запущенном приложении)](http://localhost:9999/docs)



## Особенности реализации проекта

1. Веб-приложение рабоет в связке с БД PostgreSQL.
1. Регистрация, аутентификация и авторизация юзеров выполнена с помощью fastapi-users, авторизация осуществляется с помощью JWT-токенов, размещенных в coockie браузера пользователя.
2. Реализовано кэширование запроса /all_posts через redis.
3. Реализовано развертывание в docker-compose.



   