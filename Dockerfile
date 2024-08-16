FROM python:3.12

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY pyproject.toml poetry.lock README.md .

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

RUN poetry check

RUN poetry install --no-root

COPY . .
    
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]





