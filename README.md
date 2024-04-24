# Краткое руководство по использованию Cat Charity Fund

Cat Charity Fund - это веб-приложение, позволяющее пользователям делать пожертвования на благотворительные проекты, созданные администраторами. Пожертвования автоматически распределяются по открытым проектам, пока не наберется достаточная сумма для их завершения.

## Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:OFF1GHT/cat_charity_fund.git
```


## Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

## Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Создайте файл .env:

```
APP_TITLE=Благотворительный фонд поддержки котиков
DESCRIPTION=приложение для Благотворительного фонда поддержки котиков QRKot
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=randomsecretkey
FIRST_SUPERUSER_EMAIL=admin@gmail.com
FIRST_SUPERUSER_PASSWORD=admin12345
```

## Инициализация базы данных:
```
alembic upgrade head
```

## Запуск веб-приложения:

```
uvicorn app.main:app --reload
```

## Используемые  технологии:
- FastAPI
- SQLite
- SQLAlchemy
- Google API
- Google Sheets API
- OAuth 2.0
- Python Google Auth Library