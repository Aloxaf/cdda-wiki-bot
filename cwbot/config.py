import toml

config = toml.load("config.toml")
website = config["website"]
cdda = config["cdda"]


class website:
    host = website["host"]
    path = website["path"]
    username = website["username"]
    password = website["password"]


class cdda:
    repo_dir = cdda["repo_dir"]
    task_type = cdda["task_type"]



