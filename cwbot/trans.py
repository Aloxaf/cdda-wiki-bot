import json
import gettext
import typing as t
from pathlib import Path

ZH_CN: t.Optional[gettext.GNUTranslations] = None
TRANS = {}

Entry = t.Dict[str, str | float | int | dict | list]


def npgettext(context, single, plural):
    # Fuck python 3.6, which doens't support pgettext
    if context:
        if not plural:
            text = ZH_CN.gettext(f"{context}\004{single}")
        if plural or text == single:
            text = ZH_CN.ngettext(f"{context}\004{single}", f"{context}\004{plural}", 1)
    else:
        if not single:
            return ''
        if not plural:
            text = ZH_CN.gettext(single)
        if plural or text == single:
            text = ZH_CN.ngettext(single, plural, 1)
    return single if '\004' in text else text


def extract(data: Entry):
    if isinstance(data, dict) and isinstance(data.get("id"), str):
        mid = data["id"]
        if isinstance(data.get("name"), str):
            name = data["name"]
        elif isinstance(data.get("name"), dict):
            name = data["name"]
            if name.get("str"):
                name = name["str"]
            elif name.get("str_sp"):
                name = name["str_sp"]
            else:
                return
        else:
            return
        TRANS[mid] = npgettext(None, name, None)


def init(repo_dir: str):
    """
    初始化翻译
    :param repo_dir: cdda repo 位置
    :return:
    """
    data_dir = Path(repo_dir) / "data"
    localedir = Path(repo_dir) / "lang/mo"

    global ZH_CN
    ZH_CN = gettext.translation("cataclysm-dda", localedir=localedir, languages=["zh_CN"])
    ZH_CN.install()

    for file in Path(data_dir).rglob("**/*.json"):
        data = json.load(file.open())
        if isinstance(data, list):
            for d in data:
                extract(d)
        else:
            extract(data)


def trans(text: str) -> str:
    """
    翻译 id => 中文名称
    :param text:
    :return:
    """
    return TRANS.get(text, text)
