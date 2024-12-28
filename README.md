# Проект QRkot_spreadseets QRKot


## Технологии проекта
    Совокупность языка программирования Python и фреймворка FastAPI.
    Для работы с базами данных используется SQLAlchemy совместно с Alembic - инструментом миграции баз данных.
    Использована библиотека Pydantic для проверки данных.

## Описание проекта

    Проект QRkot_spreadseets - это дополнение предыдущего проекта QRKot реализующее возможность формирования отчёта в гугл-таблице. В таблице должны быть закрытые проекты, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.
    Волонтёрам фонда нужно знать, какие проекты быстрее всего закрываются. Это поможет выделить проекты, которым нужна дополнительная реклама. Ни один котик не должен остаться без помощи!
    
## Развертывание проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:MihailKirzhakov/QRkot_spreadsheets.git

cd QRkot_spreadsheets
```

Cоздать виртуальное окружение:

```
py -3.9 -m venv venv
```

Активировать виртуальное окружение:

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
В корневой папке есть файл .env.example,
с примером того как надо заполнять .env файл.

## Запуск проекта
Применить миграции:
```
alembic upgrade head
```
Запустить проект:
```
uvicorn app.main:app
```
## Сервис будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
- http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc

## Примеры запросов к API
Все запросы делались в приложении [Postman](https://www.postman.com/)

*Создание пожертвования*
- POST donation
- http://127.0.0.1:8000/donation/
```
{
    "full_amount": 0,
    "comment": "string"
}
```
*Ответ*
```
{
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2019-08-24T14:15:22Z"
}
```
*Регистрация пользователя*
- POST user
- http://127.0.0.1:8000/auth/register
```
{
    "email": "{{firstUserEmail}}",
    "password": "{{firstUserPassword}}"
}
```
*Ответ*
```
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

Автор: [Михаил Киржаков](https://github.com/MihailKirzhakov)
