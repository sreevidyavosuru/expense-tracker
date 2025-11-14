from typing import List, Dict, Optional
from .models import Expense
from datetime import date

class ExpenseError(Exception):
    pass

class ExpenseManager:
    def __init__(self):
        self._expenses: Dict[int, Expense] = {}
        self._next_id = 1

    def add_expense(self, title: str, amount: float, category: str, exp_date: Optional[date]=None) -> Expense:
        if amount < 0:
            raise ExpenseError('Amount cannot be negative')
        if not title or not category:
            raise ExpenseError('Title and category are required')
        if exp_date is None:
            exp_date = date.today()
        e = Expense(id=self._next_id, title=title.strip(), amount=float(amount), category=category.strip(), date=exp_date)
        self._expenses[self._next_id] = e
        self._next_id += 1
        return e

    def remove_expense(self, expense_id: int) -> None:
        if expense_id not in self._expenses:
            raise ExpenseError('Expense not found')
        del self._expenses[expense_id]

    def update_expense(self, expense_id: int, **kwargs) -> Expense:
        if expense_id not in self._expenses:
            raise ExpenseError('Expense not found')
        e = self._expenses[expense_id]
        if 'amount' in kwargs:
            amount = kwargs['amount']
            if amount < 0:
                raise ExpenseError('Amount cannot be negative')
            e.amount = float(amount)
        if 'title' in kwargs:
            e.title = kwargs['title'].strip()
        if 'category' in kwargs:
            e.category = kwargs['category'].strip()
        if 'date' in kwargs:
            e.date = kwargs['date']
        return e

    def list_expenses(self) -> List[Expense]:
        return list(self._expenses.values())

    def total_spent(self) -> float:
        return sum(e.amount for e in self._expenses.values())

    def filter_by_category(self, category: str) -> List[Expense]:
        s = category.strip().lower()
        return [e for e in self._expenses.values() if e.category.lower() == s]

    def expenses_in_month(self, year: int, month: int) -> List[Expense]:
        return [e for e in self._expenses.values() if e.date.year == year and e.date.month == month]
