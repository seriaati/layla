import json
import typing

import yaml


def divide_chunks(
    li: typing.List[typing.Any], n: int
) -> typing.Generator[typing.List[typing.Any], None, None]:
    for i in range(0, len(li), n):
        yield li[i : i + n]


def get_json(dir: str) -> typing.Dict[str, typing.Any]:
    try:
        with open(dir, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_yaml(dir: str) -> typing.Dict[str, typing.Any]:
    try:
        with open(dir, "r", encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.FullLoader)  # type: ignore
    except FileNotFoundError:
        return {}
