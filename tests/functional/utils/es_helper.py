from typing import Generator
import json


def prepare_for_es_insert(data: list[dict], index: str) -> str:

    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': str(row['id'])}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'
    return str_query


def prepare_for_es_delete(data: list[dict], index: str) -> Generator:
    for obj in data:
        yield {
            '_op_type': 'delete',
            '_index': index,
            '_id': obj['id'],
        }