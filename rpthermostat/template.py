import re

try:
    from collections.abc import Callable
    from typing import Any
except ImportError:
    pass

PATTERN = re.compile("{{(.*?)}}")


def _replace(variables: dict[str, Any]) -> Callable[[Any], str]:
    def inner(match: Any) -> str:
        return str(eval(match.group(1).strip(), globals(), variables))

    return inner


def parse(path: str, **variables: Any) -> str:
    parsed = ""

    with open(path, "r") as file:
        for line in file:
            parsed += PATTERN.sub(_replace(variables), line)

    return parsed

