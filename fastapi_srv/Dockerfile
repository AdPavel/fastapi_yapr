FROM python:3.10-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
FROM base
COPY --from=builder /install /usr/local
RUN apk --no-cache add libpq

WORKDIR /fastapi_srv
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . .

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
ENTRYPOINT ["python", "./src/main.py"]
#CMD ["tail -F anything"]