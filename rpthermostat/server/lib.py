try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # pyright: ignore[reportConstantRedefinition]

if TYPE_CHECKING:
    from enum import IntEnum, StrEnum
else:
    IntEnum = object
    StrEnum = object


__all__ = ["IntEnum", "StrEnum"]
