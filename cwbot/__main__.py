from sys import argv

from .parse import CddaJsonParser
from .wiki import WikiBot


def main():
    if len(argv) != 2:
        print(f"Usage: {argv[0]} CDDA_DATA_PATH")
        exit()

    parser = CddaJsonParser(argv[1])
    parser.parse_all()
    parser.expand_inherit()

    bot = WikiBot(
        "cdda-wiki.aloxaf.cn",
        path="/",
        username="Aloxaf@auto-sync-bot",
        password="u3a5vrar77qv8ci99fq7ocbb7flmrv9f",
    )

    spells = []
    for mod, data in parser.mods.items():
        spells.extend(data.get_type("SPELL"))
    bot.update_spells(spells)


if __name__ == "__main__":
    main()
