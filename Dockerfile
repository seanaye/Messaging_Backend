FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev make libffi-dev

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apk del .build-deps gcc musl-dev make libffi-dev

ADD . / ./

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

