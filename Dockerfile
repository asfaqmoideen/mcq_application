FROM python:3.12.3

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

COPY .env /src

WORKDIR /src/src

# RUN alembic upgrade head

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
