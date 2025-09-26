FROM python:3.13

WORKDIR /usr/src/user_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .env .
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
