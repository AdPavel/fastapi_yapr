from typing import Generator, List
import json

def prepare_for_es_insert(data: list[dict], index: str) -> List:

    # for obj in data:
    #     yield {
    #         '_index': index,
    #         '_id': obj['id'],
    #         '_source': obj
    #     }

    data_to_insert = []
    for obj in data:
        index_description = {
            "index": {
                "_index": index,
                "_id": str(obj['id'])
            }
        }
        data_to_insert.append(index_description)
        data_to_insert.append(obj)

    return data_to_insert


def prepare_for_es_delete(data: list[dict], index: str) -> Generator:
    for obj in data:
        yield {
            '_op_type': 'delete',
            '_index': index,
            '_id': obj['id'],
        }