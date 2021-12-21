import typing as t
from copy import deepcopy

from loguru import logger
from .utils import get_name
from ..types import Json


def template(data: Json, mod_name: t.Optional[str] = None) -> t.Tuple[str, str]:
    """
    生成书籍模板
    :param data:
    :param mod_name:
    :return:
    """
    data = deepcopy(data)

    name = get_name(data)
    data["name"] = name

    # 生成模板
    fields = []
    for k, v in data.items():
        if k == "snippet_category":
            logger.warning("Skip snippet_category")
            return "", ""
        if k == "proficiencies":
            v = [i["proficiency"] for i in v]
        if k == "description":
            v = v["str"]
        if isinstance(v, list):
            if len(v) == 0:
                continue
            if isinstance(v[0], str):
                v = "  ".join(v)
            else:
                raise Exception(data["id"], k, v)
        fields.append(f"|{k}={v}")
    mod_str = f"|mod_name={mod_name}\n" if mod_name else ""
    return name, "<noinclude>{{Book</noinclude>\n" + mod_str + "\n".join(fields) + "\n}}\n"
