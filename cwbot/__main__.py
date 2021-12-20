from . import config
from . import trans
from .parse import CddaJsonParser
from .bot import WikiBot


def main():
    parser = CddaJsonParser(config.cdda.repo_dir)
    parser.parse_all()
    parser.expand_inherit()

    trans.init(config.cdda.repo_dir)

    bot = WikiBot(
        config.website.host,
        path=config.website.path,
        username=config.website.username,
        password=config.website.password,
    )

    for mod_id, mod in parser.mods.items():
        for task_type in config.cdda.task_type:
            data = mod.get_type(task_type)
            mod_name = mod.name
            if mod_id == "dda":
                mod_name = None
            match task_type:
                case "SPELL":
                    bot.update_spells(data, mod_name)
                case "BOOK":
                    bot.update_books(data, mod_name)


if __name__ == "__main__":
    main()
