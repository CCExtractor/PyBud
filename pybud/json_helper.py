import json


def json_to_dict(inp: str):
    return json.load(inp)


def dict_to_json(inp: dict):
    return json.dumps(inp)


def json_file_to_dict(file: str) -> dict:
    with open(file, 'r') as json_file:
        return json.load(json_file)


def dict_to_json_file(inp: dict, file: str):
    json_file = open(file, 'w')
    ret = json.dumps(inp, indent=4)  # nice formatting
    json_file.write(ret)
    json_file.close()
