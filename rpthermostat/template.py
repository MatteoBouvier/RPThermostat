import re

from udatetime import datetime  # pyright: ignore[reportImplicitRelativeImport, reportUnusedImport]

try:
    from collections.abc import Callable
    from typing import Any
except ImportError:
    pass

PATTERN = re.compile("{{(.*?)}}")


def _replace(variables: dict[str, Any]) -> Callable[[re.Match[str]], str]:
    def inner(match: re.Match[str]) -> str:
        return str(eval(match.group(1).strip(), globals(), variables))

    return inner


def parse(path: str, **variables: Any) -> str:
    parsed = ""

    with open(path, "r") as file:
        for i, line in enumerate(file, start=1):
            try:
                parsed += PATTERN.sub(_replace(variables), line)

            except NameError as e:
                raise NameError(f"Template formatting failed at line #{i}\n{line}\n{e}")

    return parsed
