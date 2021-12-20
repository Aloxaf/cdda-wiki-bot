import typing as t
from copy import deepcopy

from ..types import Json
from ..trans import trans as tr


def template(data: Json, mod_name: t.Optional[str] = None) -> t.Tuple[str, str]:
    """
    从 JSON 生成法术页面
    :param data: 一个法术 JSON
    :param mod_name: MOD 名称
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
            v = [f"[[{tr(i['id'])}]]" for i in v]
        if k == "effect":
            v = f"[[法术效果#{v}|{v}]]"
        if k == "flags":
            v = [f"[[FLAGS:法术#{i}|{i}]]" for i in v]
        if k == "valid_targets":
            v = [f"[[施法目标#{i}|{i}]]" for i in v]
        if k == "affected_body_parts":
            v = [f"[[{tr(i)}]]" for i in v]
        if isinstance(v, list):
            if isinstance(v[0], str):
                v = ", ".join(v)
            else:
                raise Exception(k, v)
        fields.append(f"|{k}={v}")
    mod_str = f"|mod_name={mod_name}\n" if mod_name else ""
    return name, "<noinclude>{{Spell</noinclude>\n" + mod_str + "\n".join(fields) + "\n}}\n"
