import re
import time

PATTERN = re.compile("%([A-Za-z])")


class datetime:
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        weekday: int,
        yearday: int,
    ):
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hour: int = hour
        self.minute: int = minute
        self.second: int = second
        self.weekday: int = weekday

    @staticmethod
    def now() -> "datetime":
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, *_ = (
            time.localtime(time.time())
        )
        return datetime(
            tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday
        )

    def _format_one(self, match: re.Match[str]) -> str:
        return {
            "A": [
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche",
            ][self.weekday],
            "w": str(self.weekday),
            "d": "{:0>2d}".format(self.day),
            "B": [
                "Janvier",
                "Février",
                "Mars",
                "Avril",
                "Mai",
                "Juin",
                "Juillet",
                "Août",
                "Septembre",
                "Octobre",
                "Novembre",
                "Décembre",
            ][self.month - 1],
            "m": "{:0>2d}".format(self.month),
            "Y": str(self.year),
            "H": "{:0>2d}".format(self.hour),
            "M": "{:0>2d}".format(self.minute),
        }[match.group(1)]

    def strftime(self, form: str) -> str:
        return PATTERN.sub(self._format_one, form)
