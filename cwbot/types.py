import typing as t

Json = t.Union[t.List['JSON'], t.Dict[t.Union[str, int], 'JSON'], str, int, float]