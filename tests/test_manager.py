import pytest
from datetime import date
from src.expense_tracker.manager import ExpenseManager, ExpenseError

@pytest.fixture
def mgr():
    return ExpenseManager()

def test_add_expense_success(mgr):
    e = mgr.add_expense('Lunch', 120.5, 'Food', date(2023,1,1))
    assert e.id == 1
    assert e.title == 'Lunch'
    assert mgr.total_spent() == pytest.approx(120.5)

def test_add_negative_amount(mgr):
    with pytest.raises(ExpenseError):
        mgr.add_expense('Bad', -10, 'Misc')

def test_remove_expense(mgr):
    e = mgr.add_expense('X', 10, 'A')
    mgr.remove_expense(e.id)
    assert mgr.list_expenses() == []

def test_remove_not_found(mgr):
    with pytest.raises(ExpenseError):
        mgr.remove_expense(999)

def test_update_expense_amount(mgr):
    e = mgr.add_expense('E', 50, 'C')
    mgr.update_expense(e.id, amount=75)
    assert mgr._expenses[e.id].amount == pytest.approx(75)

def test_filter_by_category(mgr):
    mgr.add_expense('A', 10, 'Food')
    mgr.add_expense('B', 20, 'food')
    res = mgr.filter_by_category('Food')
    assert len(res) == 2

def test_expenses_in_month(mgr):
    mgr.add_expense('Jan', 5, 'misc', date(2024,1,10))
    mgr.add_expense('Feb', 6, 'misc', date(2024,2,5))
    res = mgr.expenses_in_month(2024,1)
    assert len(res) == 1
