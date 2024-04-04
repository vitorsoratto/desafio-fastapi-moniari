import csv
import io
import json


def csv_to_json(csv_response: str) -> dict:
    '''
    Convert csv text to json
    :param csv_response:
    :return: Lowered keys json response
    '''

    reader = csv.DictReader(io.StringIO(csv_response))
    json_str = json.dumps(list(reader))
    json_response = json.loads(json_str)[0]
    json_response = {k.lower(): v for k, v in json_response.items() if v}
    return json_response
