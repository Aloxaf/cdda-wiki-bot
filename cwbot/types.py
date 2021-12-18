import typing as t

Json = t.Union[t.List['Json'], t.Dict[t.Union[str, int], 'Json'], str, int, float]
