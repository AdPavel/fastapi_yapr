FROM python:3.10-alpine as base

FROM base as builder

RUN mkdir /install
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
RUN apk --no-cache add libpq

WORKDIR /opt/app
COPY run_etl.sh run_etl.sh
COPY . .

RUN sed -i 's/\r$//g' /opt/app/run_etl.sh \
    && chmod +x  /opt/app/run_etl.sh

EXPOSE 8000
