#!/bin/sh

echo "Waiting for ElasticSearch..."

python /tests/functional/utils/wait_for_es.py

echo "ElasticSearch started"

echo "Waiting for Redis..."

python /tests/functional/utils/wait_for_redis.py

echo "Redis started"

pytest /tests/functional/src