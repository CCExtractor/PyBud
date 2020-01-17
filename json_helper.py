import json


def json_to_dict(inp: str):
    return json.load(inp)


def dict_to_json(inp: dict):
    return json.dumps(inp)


def dict_to_json_file(inp: dict, file: str):
    with open(file, 'w') as json_file:
        json.dump(str(inp), json_file)
