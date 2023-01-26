import time
from elasticsearch import Elasticsearch
import sys; sys.path.append("..")
from tests.functional.settings import settings


if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'http://{settings.els_host}:{settings.els_port}',
        validate_cert=False, use_ssl=False
    )
    while True:
        if es_client.ping():
            break
        time.sleep(1)
