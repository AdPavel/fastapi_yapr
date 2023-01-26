from settings import settings

import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'http://{settings.els_host}:{settings.els_port}',
        validate_cert=False, use_ssl=False
    )
    while True:
        if es_client.ping():
            break
        time.sleep(1)
