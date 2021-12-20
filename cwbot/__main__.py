from sys import argv

from . import trans
from .parse import CddaJsonParser
from .wiki import WikiBot


def main():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} CDDA_PATH")
        exit()

    parser = CddaJsonParser(argv[1])
    parser.parse_all()
    parser.expand_inherit()

    trans.init(argv[1] + "/data", argv[1] + "/lang/mo")

    bot = WikiBot(
        "cdda-wiki.aloxaf.cn",
        path="/",
        username="AutoUpdateBot",
        password="u3a5vrar77qv8ci99fq7ocbb7flmrv9f",
    )

    for mod, data in parser.mods.items():
        spells = data.get_type("SPELL")
        mod_name = data.name
        if mod == "dda":
            mod_name = None
        bot.update_spells(spells, mod_name)


if __name__ == "__main__":
    main()
