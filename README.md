Источник питания API
-
API для работы с промышленным источником питания.

Структура проекта:
- 
- src/
  - app/
     - dependencies.py
     - router.py
     - schemas.py
     - services.py
  - tests/
     - conftest.py
     - test_router.py
  - main.py
- .flake8
- .gitignore
- Dockerfile
- README.md
- poetry.lock
- pyproject.toml
  
Старт приложения:
-
Предварительные условия: Docker

Шаги:
1. Клонируйте репозиторий: git clone https://github.com/Laynss/fastapi.git
2. Создайте образ: docker build . -t fastapi:latest
3. Запустите контейнер: docker run -p 8000:8000 fastapi 
4. Доступ к документации API можно получить через веб-браузер по адресу: http://localhost:8000/docs#/

Использование API
-
1. Опрос данных с источника питания
  - Метод: GET
  - URL: /channels/info/{channel_id}
  - Параметры запроса:
    - channel_id (int): номер канала

2. Включение канала
  - Метод: POST
  - URL: /channels/channel/on
  - Параметры запроса:
    - number (int): Номер канала
    - voltage (float): Заданное напряжение
    - amperage (float): Заданный ток

3. Выключение канала
  - Метод: POST
  - URL: /channels/channel/off
  - Параметры запроса:
    - number (int): Номер канала

4. Получение данных о всех каналах
  - Метод: GET
  - URL: /channels/status
