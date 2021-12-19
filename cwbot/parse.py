import json
import typing as t
from pathlib import Path
from collections import defaultdict

from loguru import logger

from . import inherit
from .types import Json

BLACKLIST = {
    "ammunition_type",
    "city_building",
    "overmap_terrain",
    "monstergroup",
    "mapgen",
    "charge_removal_blacklist",
    "colordef",
    "dream",
    "EXTERNAL_OPTION",
    "hit_range",
    "ITEM_BLACKLIST",
    "mod_tileset",
    "mood_face",
    "monster_adjustment",
    "MIGRATION",
    "MONSTER_BLACKLIST",
    "MONSTER_FACTION",
    "MONSTER_WHITELIST",
    "obsolete_terrain",
    "overlay_order",
    "overmap_land_use_code",
    "profession_item_substitutions",
    "region_overlay",
    "rotatable_symbol",
    "requirement",
    "scenario",
    "SCENARIO_BLACKLIST",
    "speech",
    "skill_boost",
    "snippet",
    "start_location",
    "talk_topic",
    "TRAIT_BLACKLIST",
    "uncraft",
}


class Mod:
    def __init__(self, modinfo: Json):
        modinfo = modinfo[0]
        assert modinfo["type"] == "MOD_INFO"
        self.cid = modinfo["id"]
        self.name = modinfo["name"]
        self.dependencies = modinfo.get("dependencies", [])
        # 存放 JSON 数据，key 为 ID
        self.items: t.Dict[str, Json] = {}
        self.types: t.Dict[str, t.List[Json]] = defaultdict(list)

    def get(self, cid: str) -> t.Optional[Json]:
        """
        从 MOD 中查找指定 ID 的物品
        :param cid: 物品 ID
        :return: 物品
        """
        return self.items.get(cid)

    def get_type(self, type_id: str) -> t.List[Json]:
        """
        从 MOD 中查找指定类型的物品
        :param type_id: 物品
        :return: 物品列表
        """
        return self.types.get(type_id, [])

    def add(self, items: t.List[Json]):
        """
        增加物品到该 MOD 中
        :param items: 从 JSON 中读取的数据，应该是一个 list
        :return:
        """
        assert isinstance(items, list)
        # 此处可能会将 MOD_INFO 也加入进去，不过应该没有副作用
        for item in items:
            if item.get("type") == "recipe":
                # TODO: 因为配方的 result 可能有多个，所以此处暂时没有记录配方
                continue
            elif item.get("type") in BLACKLIST:
                continue
            else:
                cid = item.get("id") or item.get("abstract")
                if not cid:
                    logger.warning("skip {}", item.get("type"))
                    continue
                if not isinstance(cid, str):
                    print(cid)
                self.items[cid] = item
                self.types[item["type"]].append(item)


class CddaJsonParser:
    def __init__(self, data_dir: str):
        """
        初始化解析器
        :param data_dir: data 文件夹的位置
        """
        self.data_dir = Path(data_dir)
        self.mods: t.Dict[str, Mod] = dict()

    def parse_all(self):
        """
        将所有 JSON 读取到内存中，并自动处理 copy-from 等关系
        :return:
        """
        for path in self.paths_to_parse():
            # 首先读取文件夹下的 modinfo.json，记录 MOD 数据
            if path.name.endswith("core") or path.name.endswith("json"):
                mod_id = "dda"
            elif (modinfo := (path / "modinfo.json")) and modinfo.exists():
                modinfo = json.load(modinfo.open())
                mod_id = modinfo[0]["id"]
                if not self.mods.get(mod_id):
                    self.mods[mod_id] = Mod(modinfo)
            else:
                raise FileNotFoundError(f"No modinfo.json found in {path}")

            # 写入 self.mods 中
            for file in path.rglob("**/*.json"):
                data = json.load(file.open())
                self.mods[mod_id].add(data)

    def expand_inherit(self):
        """
        展开所有的 JSON 继承
        :return:
        """
        # 重复展开，直到没有东西可以展开

        for i in range(5):
            logger.info("正在展开继承属性")
            success = False
            for mod_id, mod in self.mods.items():
                find_in = [mod_id]
                find_in.extend(mod.dependencies)
                for item in mod.items.values():
                    if not item.get("copy-from"):
                        continue
                    success = True
                    copy_from_id = item["copy-from"]
                    copy_from_item = self.find_by_id(copy_from_id, find_in)
                    try:
                        inherit.expand(item, copy_from_item)
                    except Exception as e:
                        logger.exception("{} 展开失败：{}", item.get("id"), e)
            if not success:
                return

    def find_by_id(self, cid: str, mods: t.List[str]) -> Json:
        """
        从指定 MOD 中查物品
        :param cid: 物品 ID
        :param mods: MOD 列表
        :return: 物品
        """
        for mod in mods:
            if x := self.mods[mod].get(cid):
                return x

    def paths_to_parse(self) -> t.List[Path]:
        """
        获取需要扫描的文件夹
        :return:
        """
        # dda MOD 放在最前面，因为需要从里面读取 dda MOD 的信息
        paths = [
            self.data_dir / "mods/dda",
            self.data_dir / "core",
            self.data_dir / "json",
        ]

        for entry in (self.data_dir / "mods").iterdir():
            if entry.is_file():
                continue
            if entry.name in {"TEST_DATA", "dda"}:
                continue
            paths.append(entry)

        return paths
