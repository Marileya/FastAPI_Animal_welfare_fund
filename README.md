# Итоговый проект по разделу FastAPI
### Пожертвования для котиков

В этом проекте выполнено следующее:
- настроены модели для БД,
- применены миграции с помощью Alembic,
- созданы схемы для запроса и ответа с помощью Pydantic,
- настроена аутентификация и авторизация пользователей,
- описаны доступные эндпоинты.


#### Этот проект предусматривает следующие возможности:

Создание, редактирование и удаление проектов (только суперпользователь). Важно! Удалить можно лишь тот проект, который еще не получил ни одного доната и не закрыт.
Создание пожертвования (все зарегистрированные пользователи).
Получение списка своих пожервтований (для зарегистрированного).

*Изменение и удаление пожертвований ЗАПРЕЩЕНО всем (конечно лишь при обращении к API...).* 

Для получения информации о всех возможностях API необходимо использовать документацию из файла 

## Примеры запросов
##### GET-запрос на https://localhost/charity_project/

<b>Request:</b> None
Для всех пользователей

<b>Response:</b>

```json
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
  }
]
```

##### DELETE-запрос на https://localhost/charity_project/{project_id}

Только для Суперпользователя
<b>Request:</b> None
<b>Response:</b>

```json
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
  }
```

##### POST-запрос на https://localhost/donation/
Только для Авторизованных пользователей
<b>Request:</b>

```json
{
"full_amount": 0,
"comment": "string"
}
```

<b>Response:</b>

```json
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2019-08-24T14:15:22Z"
}
```

##### GET-запрос на https://localhost/donation/
Только для Суперпользователя
<b>Request:</b> None

<b>Response:</b>

```json
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2019-08-24T14:15:22Z",
    "user_id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "close_date": "2019-08-24T14:15:22Z"
  }
]
```

## Запуск проекта
Все стандартно и просто
1) Копируем проект на свой компьютер

```bash
git clone <ссылка на проект на GitHub>
```

2) Устанавливаем и активируем виртуальное окружение в папаке с проектом

```bash
python -m venv venv
source venv/Scripts/activate
```

3) Устанавливаем все зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

Скорее всего потребуется обновить pip (команду подсмотрите в терминале)

4) Примените миграции из папки alembic

```bash
alembic upgrade head
```

5) Запустите проект

```bash
uvicorn app.main:app
```