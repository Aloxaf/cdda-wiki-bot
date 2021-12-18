import json
import typing as t
from collections import defaultdict
from pathlib import Path

Json = t.Union[t.List['JSON'], t.Dict[t.Union[str, int], 'JSON'], str, int, float]


class CddaJsonParser:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data = defaultdict(default_factory=dict)

    def parse_all_json(self):
        """
        将所有 JSON 读取到内存中，并自动处理 copy-from 等关系
        :return:
        """
        for path in self.get_data_paths():
            if path.name.endswith("core") or path.name.endswith("json"):
                modname = "dda"
            elif (modinfo := (path / "modinfo.json")) and modinfo.exists():
                modinfo = json.load(modinfo.open())
                modname = modinfo[0]["name"]

            for file in path.rglob("**/*.json"):
                data: t.List[Json] = json.load(file.open())

                for d in data:
                    if d.get("type") == "SPELL":
                        print(d)

    def get_data_paths(self) -> t.List[Path]:
        """
        获取需要扫描的文件夹
        :return:
        """
        paths = [self.data_dir / "data/core", self.data_dir / "data/json"]

        for entry in (self.data_dir / "mods").iterdir():
            if entry.is_file():
                continue
            if entry.name == "TEST_DATA":
                continue
            paths.append(entry)

        return paths
