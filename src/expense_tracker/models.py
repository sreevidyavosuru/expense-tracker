from dataclasses import dataclass, asdict
from datetime import date

@dataclass
class Expense:
    id: int
    title: str
    amount: float
    category: str
    date: date = date.today()

    def to_dict(self):
        d = asdict(self)
        d['date'] = self.date.isoformat()
        return d
