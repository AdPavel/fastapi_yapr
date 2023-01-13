import logging
import datetime
from typing import Generator

import backoff
import psycopg2
from psycopg2.extensions import connection


class PostgresExtractor:

    def __init__(self, conn: connection, batch_size: int) -> None:
        self.connection = conn
        self.batch_size = batch_size

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(psycopg2.Error, psycopg2.OperationalError)
    )
    def get_modified_objects(self, modified_date: str, query_desc: dict) -> Generator[list, None, None]:

        cursor = self.connection.cursor()
        if not modified_date:
            modified_date = datetime.datetime.min

        query = query_desc['query']
        variables_amount = query_desc['variables_amount']

        cursor.execute(query, (modified_date,) * variables_amount)
        logging.info('Ready to get data from Postgres')

        while data := cursor.fetchmany(self.batch_size):
            logging.info('Get {len} objects'.format(len=len(data)))
            yield data
