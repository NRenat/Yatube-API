# Yatube API:
API для проекта YaTube.

Написано на Django и Django REST Framework. Позволяет управлять постами, комментариями, аутентификацией, группами, подписками.

API позволяет функционал сайта другими сайтами и приложениями, а аутентификация по JWT-токенам обеспечивает безопасность и надежность.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/NRenat/api_final_yatube.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Примеры запросов к API:

```
/api/v1/posts/?limit=2&offset=4 

Ответ:
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/v1/posts/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "id": 2,
            "author": "regular_user",
            "text": "SomeText",
            "pub_date": "2023-09-15T18:59:22.269330Z",
            "image": null,
            "group": 1
        }
    ]
}
```

## Технологии
* Python 3.9
* Django
* DRF
* simplejwt
* djoser
