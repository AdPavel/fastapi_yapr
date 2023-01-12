import argparse
import logging
from datetime import datetime

import psycopg2
import redis
from elasticsearch import Elasticsearch
from psycopg2.extras import RealDictCursor

from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from models import Movie
from queries import modified_movies_query
from settings import els_configs
from settings import postgres_configs
from settings import redis_configs
from state import RedisStorage
from state import State
from transformer import DataTransformer


def main():

    parser = argparse.ArgumentParser(description='Load data from postgres to elasticsearch')
    parser.add_argument('-md', '--modified_date', type=str, help='Define a modified date')
    args = parser.parse_args()

    modified_date = args.modified_date

    logging.basicConfig(level=logging.INFO)

    els_index = 'movies'
    els_schema_path = 'els_schema.json'

    redis_adapter = redis.Redis(
        host=redis_configs.redis_host, port=redis_configs.redis_port,
        db=redis_configs.redis_db, decode_responses=True
    )

    state_storage = RedisStorage(redis_adapter)
    state = State(state_storage)

    if not modified_date:
        modified_date = state.get_state('modified_date')
    logging.info('Modified_date {modified_date}'.format(modified_date=modified_date))

    with psycopg2.connect(**postgres_configs.dict(), cursor_factory=RealDictCursor) as pg_conn:
        postgres_extractor = PostgresExtractor(pg_conn, 100)
        logging.info('Create connection with Postgres')
        movies_batches = postgres_extractor.get_modified_objects(modified_date, modified_movies_query)

    try:
        data_transformer = DataTransformer(els_index, Movie)

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

        for movies in movies_batches:
            if movies:
                transformed_movies = data_transformer.transform_data(movies)
                data_loader.bulk_create(transformed_movies)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.set_state('modified_date', now)
        logging.info('Set state to {datetime}'.format(datetime=now))

    finally:
        pg_conn.close()


if __name__ == '__main__':
    main()
