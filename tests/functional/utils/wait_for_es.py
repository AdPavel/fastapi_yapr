from elasticsearch import Elasticsearch
import sys
import os
import backoff
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import settings


@backoff.on_exception(
    wait_gen=backoff.expo, exception=Exception
)
def wait_for_es():
    es_client = Elasticsearch(
        hosts=f'http://{settings.els_host}:{settings.els_port}',
        validate_cert=False, use_ssl=False
    )
    ping = es_client.ping()
    if ping:
        return ping
    raise Exception


if __name__ == '__main__':

    wait_for_es()
