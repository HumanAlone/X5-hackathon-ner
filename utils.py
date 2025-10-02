import ast
from typing import List
from pydantic import BaseModel


class EntityResponse(BaseModel):
    start_index: int
    end_index: int
    entity: str


def convert_model_output(model_output: str) -> List[EntityResponse]:
    """
    Преобразует строку типа "[(0, 9, 'B-TYPE'), (10, 16, 'I-TYPE')]"
    в формат API
    """
    if not model_output or ";" not in model_output:
        return []

    list_str = model_output.split(";", 1)[1].strip()

    try:
        predictions = ast.literal_eval(list_str)

        result = []
        for start, end, entity in predictions:
            result.append(
                EntityResponse(start_index=start, end_index=end, entity=entity)
            )
        return result
    except:
        return []
