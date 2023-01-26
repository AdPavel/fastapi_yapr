FROM python:3.10-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
FROM base
COPY --from=builder /install /usr/local
RUN apk --no-cache add libpq

WORKDIR /tests
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip --default-timeout=100 future \
    && pip install -r requirements.txt
COPY . /tests/functional

RUN chmod +x  /tests/functional/run_tests.sh
