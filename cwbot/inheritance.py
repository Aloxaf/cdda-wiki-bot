from .types import Json

WHITELIST = {
    "GENERIC",
    "AMMO",
    "ARMOR",
    "BOOK",
    "COMESTIBLE",
    "ENGINE",
    "furniture",
    "GUN",
    "GUNMOD",
    "MAGAZINE",
    "MATERIAL",
    "MONSTER",
    "MONSTER_FACTION",
    "mutation",
    "overmap_terrain",
    "recipe",
    "terrain",
    "TOOL",
    "uncraft",
    "vehicle_part",
}


def expand(src: Json, dst: Json) -> bool:
    """
    处理 JSON 继承关系，规则见：
    https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/JSON_INHERITANCE.md
    https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/JSON_INFO.md#copy-from-and-abstract

    :param src: 原始 JSON，包含需要被处理的 copy-from、relative 等字段
    :param dst: copy-from 指向的 JSON
    :return: 如果 dst 中含有未处理的继承字段，则返回 False，否则返回 True
    """
    if dst.get("copy-from"):
        return False

    dst_id = dst.get("id") or dst.get("abstract")
    assert dst_id == src["copy-from"], "copy-from doens't match"
    assert dst["type"] == src["type"], "type mismatch"
    assert src["type"] in WHITELIST, f"{src['type']} not in whitelist"

    # 处理 copy-from
    for k, v in dst.items():
        if not src.get(k):
            src[k] = v
    del src["copy-from"]

    # 处理 relative
    if src.get("relative"):
        for k, v in src["relative"].items():
            if isinstance(v, float) or isinstance(v, int):
                src[k] += v
            elif isinstance(v, dict):
                # 嵌套情况
                for _k, _v in v.items():
                    if isinstance(_v, float) or isinstance(_v, int):
                        src[k][_k] += _v
                    elif isinstance(_v, str):
                        pass
                    else:
                        raise TypeError(f"Unknown Type：{type(_v)}")
            else:
                raise TypeError("Unknown Type！")
        del src["relative"]

    # 处理 proportional
    if src.get("proportional"):
        for k, v in src["proportional"].items():
            src[k] *= v
        del src["proportional"]

    # 处理 extend
    if src.get("extend"):
        for k, v in src["extend"].items():
            if not src.get(k):
                src[k] = []
            if isinstance(v, str):
                src[k].append(v)
            else:
                src[k].extend(v)
        del src["extend"]

    # 处理 delete
    if src.get("delete"):
        for k, v in src["delete"].items():
            src[k] = list(set(src[k]) - set(v))
        del src["delete"]

    return True
