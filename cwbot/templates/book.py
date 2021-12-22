import typing as t
from copy import deepcopy

from loguru import logger
from . import utils
from ..types import Json


def template(data: Json, mod_name: t.Optional[str] = None) -> t.Tuple[str, str]:
    """
    生成书籍模板
    :param data:
    :param mod_name:
    :return:
    """
    data = deepcopy(data)

    name = utils.get_name(data)
    data["name"] = name

    # 生成模板
    fields = []
    for k, v in data.items():
        match k:
            case "//":
                continue
            case "weight":
                v = utils.normalize_weight(v)
            case "volume":
                v = utils.normalize_volume(v)
            case "time":
                v = utils.normalize_time(v)
            case "price" | "price_postapoc":
                v = utils.normalize_price(v)
            case "snippet_category":
                logger.warning("Skip snippet_category")
                return "", ""
            case "proficiencies":
                v = [i["proficiency"] for i in v]
            case "description" if isinstance(v, dict):
                v = v["str"]
            case "use_action" if isinstance(v, dict):
                if v["type"] == "learn_spell":
                    k = "learn_spell"
                    v = v["spells"]
                else:
                    raise Exception(data["id"], k, v)

        if isinstance(v, list):
            if len(v) == 0:
                continue
            if isinstance(v[0], str):
                v = " ".join(v)
            else:
                raise Exception(data["id"], k, v)
        fields.append(f"|{k}={v}")
    mod_str = f"|mod_name={mod_name}\n" if mod_name else ""
    return name, "<noinclude>{{Book</noinclude>\n" + mod_str + "\n".join(fields) + "\n}}\n"
