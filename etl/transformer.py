import logging

from pydantic import BaseModel
from pydantic.schema import List


class DataTransformer:
    def __init__(self, index: str, template_class: BaseModel) -> None:
        self.index = index
        self.template_class = template_class

    def get_class_objects(self, row_data: List[tuple]) -> List[BaseModel]:

        prepared_data = []

        for obj in row_data:
            obj_description = {key: value for key, value in obj.items()}
            prepared_obj = self.template_class(**obj_description)
            prepared_data.append(prepared_obj)
        return prepared_data

    def transform_data(self, row_data: list) -> List[dict]:

        result = [obj.dict() for obj in self.get_class_objects(row_data)]
        logging.info('Transformed data')
        return result
