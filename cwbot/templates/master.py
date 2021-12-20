import typing as t
from collections import defaultdict

from ..types import Json
from ..trans import trans as tr

TEMPLATE = """{{{{Navbox
|name       = 法术体系
|title      = [[法术体系]]
|state      = uncollapsed <!-- leave blank to autocollapse -->

|bodystyle = background:#fdfdfd; width:100%; vertical-align:middle; border-color: #1a9c9c;
|titlestyle = background:#BA55D3; color:#006600; padding-left:0.3em; padding-right:0.3em; text-align:center;
|groupstyle = background:#BA55D3; color:#006600; padding-left:1em; padding-right:1em; text-align:right; font-weight: bold;

{text}

}}}}<noinclude>
[[Category:Navigational templates]]
</noinclude>"""


def sort_by_spell_class(d: Json) -> str:
    return tr(d.get("spell_class", ""))


def template(datas: t.List[Json]) -> str:
    """
    生成「模板:法术体系」
    :param datas: 法术列表
    :return: 「模板:法术体系」页面的内容
    """
    master = defaultdict(list)
    for data in sorted(datas, key=sort_by_spell_class):
        if not data.get("id"):
            continue

        spell_class = data.get("spell_class", "NONE")
        if spell_class == "NONE":
            continue

        master[spell_class].append(data["id"])

    fields = []
    for i, (master, spells) in enumerate(master.items()):
        spell_list = "{{md}}".join(f"[[{tr(spell)}]]" for spell in spells)
        fields.append(f"|group{i+1}=[[{tr(master)}]]")
        fields.append(f"|list{i+1}={spell_list}")

    return TEMPLATE.format(text="\n".join(fields))
