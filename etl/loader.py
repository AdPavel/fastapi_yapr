import json
import logging

import backoff
from elasticsearch import ConnectionError
from elasticsearch import Elasticsearch
from pydantic.schema import List
from urllib3.exceptions import HTTPError


class ElasticsearchLoader:
    def __init__(self, conn: Elasticsearch, index: str, schema_path: str) -> None:
        self.connection = conn
        self.index = index
        self.schema_path = schema_path

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=(ConnectionError, HTTPError),
        max_tries=10
    )
    def create_index(self) -> None:

        with open(self.schema_path, 'r') as file:
            schema = json.load(file)
        self.connection.indices.create(index=self.index, body=schema)
        logging.info('Create index for ElasticSearch')

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=(ConnectionError, HTTPError),
        max_tries=10
    )
    def bulk_create(self, data: List[dict]) -> None:

        data_to_insert = []
        for obj in data:
            index_description = {
                "index": {
                    "_index": self.index,
                    "_id": str(obj['id'])
                }
            }
            data_to_insert.append(index_description)
            data_to_insert.append(obj)

        self.connection.bulk(index=self.index, body=data_to_insert)
        logging.info(
            'Insert {len} objects to ElasticSearch'.format(len=len(data_to_insert) / 2)
        )
