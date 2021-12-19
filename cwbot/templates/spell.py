from ..types import Json

from typing import Tuple
from copy import deepcopy


def template(data: Json) -> Tuple[str, str]:
    """
    从 JSON 生成法术页面
    :param data: 一个法术 JSON
    :return: 该页面的名字和内容
    """
    data = deepcopy(data)

    if isinstance(data["name"], dict):
        data["name"] = data["name"]["str"]

    name = data["name"]

    # 生成模板
    fields = []
    for k, v in data.items():
        if k == "extra_effects":
            v = [i['id'] for i in v]
        if isinstance(v, list):
            if isinstance(v[0], str):
                v = ", ".join(v)
            else:
                raise Exception(k, v)
        fields.append(f"{k}={v}")
    return name, "<noinclude>{{Spell</noinclude>\n|" + "\n|".join(fields) + "\n}}\n"
