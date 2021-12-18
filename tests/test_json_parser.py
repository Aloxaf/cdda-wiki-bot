from cwbot.parse import CddaJsonParser


def test_get_data_paths(cdda_data_path: str):
    p = CddaJsonParser(cdda_data_path)
    result = p.get_data_paths()
    assert isinstance(result, list)
    print(result)


def test_parse_all_json(cdda_data_path: str):
    p = CddaJsonParser(cdda_data_path)
    result = p.parse_all_json()
    print(result)
