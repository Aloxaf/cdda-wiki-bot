from ..types import Json
from pint import UnitRegistry

ureg = UnitRegistry()
ureg.define("kUSD = 1000 * USD")
ureg.define("USD = 100 * cent")
ureg.define("cent = [dollar]")


def get_name(data: Json) -> str:
    name = data["name"]
    if isinstance(name, dict):
        if name.get("str"):
            name = name["str"]
        elif name.get("str_sp"):
            name = name["str_sp"]
    assert isinstance(name, str)
    return name


def normalize_weight(s: str, target="kg") -> str:
    return "{:g}".format(ureg(s).to(target).magnitude)


def normalize_volume(s: str, target="L") -> str:
    return "{:g}".format(ureg(s).to(target).magnitude)


def normalize_time(s: str, target="min") -> str:
    if isinstance(s, int):
        s = f"{s} m"
    s = s.replace("h", "hour").replace("m", "min")
    return "{:g}".format(ureg(s).to(target).magnitude)


def normalize_price(s: str, target="USD") -> str:
    if isinstance(s, int):
        s = f"{s} cent"
    return "{:g}".format(ureg(s).to(target).magnitude)
