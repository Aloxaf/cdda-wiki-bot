import json
from pprint import pprint

from cwbot import inherit
from cwbot.types import Json

ITEM_223 = """
{
    "id": "223",
    "type": "AMMO",
    "name": { "str_sp": ".223 Remington" },
    "description": ".223 Remington ammunition...",
    "weight": "12 g",
    "volume": "194 ml",
    "price": 280,
    "price_postapoc": 900,
    "flags": [ "IRREPLACEABLE_CONSUMABLE" ],
    "material": [ "brass", "powder" ],
    "symbol": "=",
    "color": "yellow",
    "count": 30,
    "stack_size": 47,
    "ammo_type": "223",
    "casing": "223_casing",
    "range": 36,
    "damage": { "damage_type": "bullet", "amount": 44, "armor_penetration": 2 },
    "dispersion": 30,
    "recoil": 1500,
    "effects": [ "COOKOFF" ]
}
"""
ITEM_556 = """
{
    "id": "556",
    "copy-from": "223",
    "type": "AMMO",
    "name": { "str_sp": "5.56 NATO M855" },
    "description": "5.56x45mm ammunition ...",
    "price": 290,
    "price_postapoc": 900,
    "flags": [ "IRREPLACEABLE_CONSUMABLE" ],
    "relative": { "damage": { "damage_type": "bullet", "amount": -3, "armor_penetration": 4 }, "dispersion": 140 },
    "proportional": { "recoil": 1.1 },
    "extend": { "effects": [ "NEVER_MISFIRES" ] }
}
"""
ITEM_reloaded_556 = """
{
    "id": "reloaded_556",
    "copy-from": "556",
    "type": "AMMO",
    "name": "reloaded 5.56 NATO",
    "proportional": { "price": 0.7, "damage": { "damage_type": "bullet", "amount": 0.9 }, "dispersion": 1.1 },
    "extend": { "effects": [ "RECYCLED" ] },
    "delete": { "effects": [ "NEVER_MISFIRES" ] }
}
"""
ITEM_556: Json = json.loads(ITEM_556)
ITEM_223: Json = json.loads(ITEM_223)
ITEM_reloaded_556: Json = json.loads(ITEM_reloaded_556)


def test_inheritance():
    result = inherit.expand(ITEM_reloaded_556, ITEM_556)
    assert result is False

    result = inherit.expand(ITEM_556, ITEM_223)
    assert result is True

    # copy
    assert ITEM_556["count"] == ITEM_223["count"]
    # relative
    assert ITEM_556["damage"]["amount"] == ITEM_223["damage"]["amount"] - 3
    # proportional
    assert ITEM_556["recoil"] == ITEM_223["recoil"] * 1.1
    # extend
    assert "NEVER_MISFIRES" in ITEM_556["effects"]
    # delete

    result = inherit.expand(ITEM_reloaded_556, ITEM_556)
    assert result is True
    assert "NEVER_MISFIRES" not in ITEM_reloaded_556["effects"]

    pprint(ITEM_556)
