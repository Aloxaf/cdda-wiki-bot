import typing as t

Json = t.List['Json'] | t.Dict[int | str, 'Json'] | str | int | float
