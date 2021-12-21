from ..types import Json


def get_name(data: Json) -> str:
    name = data["name"]
    if isinstance(name, dict):
        if name.get("str"):
            name = name["str"]
        elif name.get("str_sp"):
            name = name["str_sp"]
    assert isinstance(name, str)
    return name
