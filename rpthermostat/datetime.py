import re
import time

PATTERN = re.compile("%([A-Za-z])")

class datetime:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int, weekday: int, yearday: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.weekday = weekday
    
    @staticmethod
    def now() -> datetime:
        return datetime(*time.localtime(time.time()))
    
    def _format_one(self, match) -> str:       
        return {'A': ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][self.weekday],
                'w': str(self.weekday),
                'd': f"{self.day:0>2}",
                'B': ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"][self.month-1],
                'm': f"{self.month:0>2}",
                'Y': str(self.year),
                'H': f"{self.hour:0>2}",
                'M': f"{self.minute:0>2}"}[match.group(1)]
    
    def strftime(self, form: str) -> str:
        return PATTERN.sub(self._format_one, form)