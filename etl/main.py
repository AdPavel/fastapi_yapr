import argparse
import logging
from datetime import datetime

import psycopg2
import redis
from elasticsearch import Elasticsearch
from psycopg2.extras import RealDictCursor

from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from models import transform_models
from queries import sql_queries
from settings import els_configs
from settings import postgres_configs
from settings import redis_configs
from state import RedisStorage
from state import State
from transformer import DataTransformer


def main():

    parser = argparse.ArgumentParser(description='Load data from postgres to elasticsearch')
    parser.add_argument('index_name', type=str, help='Define an index to load')
    parser.add_argument('-md', '--modified_date', type=str, help='Define a modified date')
    args = parser.parse_args()

    modified_date = args.modified_date
    els_index = args.index_name

    logging.basicConfig(level=logging.INFO)
    logging.info('Start loading data for {els_index}'.format(els_index=els_index))

    els_schema_path = 'els_schemas/{els_index}.json'.format(els_index=els_index)

    redis_adapter = redis.Redis(
        host=redis_configs.redis_host, port=redis_configs.redis_port,
        db=redis_configs.redis_db, decode_responses=True
    )

    state_storage = RedisStorage(redis_adapter)
    state = State(state_storage)
    state_key_name = 'modified_date_{els_index}'.format(els_index=els_index)

    if not modified_date:
        modified_date = state.get_state(state_key_name)
    logging.info('{state_key_name} is {modified_date}'.format(
        state_key_name=state_key_name,
        modified_date=modified_date)
    )

    with psycopg2.connect(**postgres_configs.dict(), cursor_factory=RealDictCursor) as pg_conn:
        psycopg2.extras.register_uuid()
        postgres_extractor = PostgresExtractor(pg_conn, 100)
        logging.info('Create connection with Postgres')
        data_batches = postgres_extractor.get_modified_objects(modified_date, sql_queries[els_index])

    try:
        data_transformer = DataTransformer(els_index, transform_models[els_index])

        els_connection = Elasticsearch(
            'http://{host}:{port}'.format(
                host=els_configs.els_host,
                port=els_configs.els_port
            )
        )

        logging.info('Create connection with ElasticSearch')
        data_loader = ElasticsearchLoader(els_connection, els_index, els_schema_path)

        if not els_connection.indices.exists(index=els_index):
            data_loader.create_index()

        for data in data_batches:
            if data:
                transformed_data = data_transformer.transform_data(data)
                data_loader.bulk_create(transformed_data)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.set_state(state_key_name, now)
        logging.info('Set {state_key_name} to {datetime}'.format(state_key_name=state_key_name, datetime=now))

    finally:
        pg_conn.close()


if __name__ == '__main__':
    main()
