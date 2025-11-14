# Simple demo CLI to interact with ExpenseManager for manual testing
import sys
from datetime import datetime
from .manager import ExpenseManager, ExpenseError

HELP = 'Commands: add <title> <amount> <category> [YYYY-MM-DD], list, total, filter <category>, remove <id>, update <id> <field>=<value>, quit'

def demo():
    mgr = ExpenseManager()
    print('Expense Tracker Demo. Type help for commands.')
    while True:
        cmd = input('> ').strip()
        if not cmd:
            continue
        if cmd in ('q','quit','exit'):
            print('Bye'); sys.exit(0)
        if cmd == 'help':
            print(HELP); continue
        parts = cmd.split()
        if parts[0] == 'add':
            try:
                title = parts[1]
                amount = float(parts[2])
                category = parts[3]
                dt = None
                if len(parts) >=5:
                    dt = datetime.fromisoformat(parts[4]).date()
                e = mgr.add_expense(title, amount, category, dt)
                print('Added:', e.to_dict())
            except Exception as ex:
                print('Error:', ex)
        elif parts[0] == 'list':
            for e in mgr.list_expenses():
                print(e.to_dict())
        elif parts[0] == 'total':
            print('Total spent:', mgr.total_spent())
        elif parts[0] == 'filter' and len(parts)==2:
            for e in mgr.filter_by_category(parts[1]):
                print(e.to_dict())
        elif parts[0] == 'remove' and len(parts)==2:
            try:
                mgr.remove_expense(int(parts[1])); print('Removed')
            except Exception as ex:
                print('Error:', ex)
        elif parts[0] == 'update' and len(parts)>=3:
            try:
                eid = int(parts[1])
                kv = parts[2].split('=')
                field, val = kv[0], kv[1]
                kwargs = {}
                if field == 'amount':
                    kwargs['amount'] = float(val)
                elif field == 'title':
                    kwargs['title'] = val
                elif field == 'category':
                    kwargs['category'] = val
                else:
                    print('Unknown field'); continue
                mgr.update_expense(eid, **kwargs)
                print('Updated:', mgr._expenses[eid].to_dict())
            except Exception as ex:
                print('Error:', ex)
        else:
            print('Unknown command. Type help.')

if __name__ == '__main__':
    demo()
