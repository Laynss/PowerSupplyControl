Старт приложения:

Предварительные условия:
Докер

Шаги:
1. Клонируйте репозиторий: git clone https://github.com/Laynss/fastapi.git
2. Создайте образ: docker build . -t fastapi:latest
3. Запустите контейнер: docker run -p 8000:8000 fastapi 
4. Доступ к документации API можно получить через веб-браузер по адресу: http://localhost:8000/docs#/
