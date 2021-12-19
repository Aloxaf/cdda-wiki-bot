import re
import typing as t
from copy import deepcopy
from operator import add, mul

from loguru import logger
from .types import Json


def relative(src: Json, key: str, op: t.Callable[[t.Any, t.Any], t.Any]):
    if src.get(key):
        for k, v in src[key].items():
            if isinstance(v, float) or isinstance(v, int):
                # key 有可能不存在，或者类型不匹配
                if type(src.get(k)) is not type(v):
                    continue
                if not isinstance(src[k], str):
                    src[k] = op(src[k], v)
                else:
                    # 有可能是 "25 ml" 这种形式，此时只需要扩大前面的数字即可
                    n, unit = re.findall(r'([0-9.]+|\w+)', src[k])
                    src[k] = str(op(float(n), v)) + f" {unit}"
            elif isinstance(v, dict):
                # 嵌套情况
                for _k, _v in v.items():
                    # 为什么会出现 key 不存在的情况？？？
                    if type(src[k].get(_k)) is not type(_v):
                        continue
                    if isinstance(_v, float) or isinstance(_v, int):
                        src[k][_k] = op(src[k][_k], _v)
                    elif isinstance(_v, str):
                        pass
                    else:
                        logger.warning(f"Unknown Type：{type(_v)}")
            else:
                logger.warning("Unknown Type：{}", type(v))
        del src[key]


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

    if dst_id != src["copy-from"]:
        raise TypeError("copy-from doesn't match for {}: {} != {}".format(src["id"], src["copy-from"], dst_id))

    # 处理 copy-from
    for k, v in dst.items():
        if k == "id" or k == "abstract":
            continue
        if not src.get(k):
            src[k] = deepcopy(v)
    del src["copy-from"]

    # 处理 relative
    relative(src, "relative", add)

    # 处理 proportional
    relative(src, "proportional", mul)

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
            if not src.get(k):
                continue
            src[k] = [n for n in src[k] if n not in v]
        del src["delete"]

    return True
