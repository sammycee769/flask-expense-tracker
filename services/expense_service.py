from datetime import datetime

from exceptions.expense_exceptions import *
from models.expense import Expense
from repositories.expense_repo import *
from repositories.user_repo import get_user_by_id


def create_expense(data,user_id):
    get_user_by_id(user_id)
    if not data:
        raise InvalidExpenseException("Required data is missing")
    __validate_expense(data)
    date_str = data["date"]
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        raise InvalidExpenseException("Invalid date format YYYY-MM-DD")
    expense = Expense(
        amount = data["amount"],
        category = data["category"],
        date = date,
        user_id = user_id
    )
    return save(expense)

def fetch_all_expenses(user_id):
    get_user_by_id(user_id)
    expenses = get_all_expenses_by_user(user_id)
    if not expenses:
        raise ExpenseNotFoundException("No expenses found for this user")
    return expenses

def get_expense_by_category(user_id, category):
    get_user_by_id(user_id)
    expenses = get_expenses_by_category(user_id, category)

    if not expenses:
        raise ExpenseNotFoundException("No expenses found for this category")

    return expenses

def get_expense_by_date(user_id, date):
    get_user_by_id(user_id)
    expenses = get_expenses_by_date(user_id, date)

    if not expenses:
        raise ExpenseNotFoundException("No expenses found for this date")

    return expenses

def delete_expense(expense_id,user_id):
    get_user_by_id(user_id)
    expense = __get_validated_expense(expense_id, user_id)
    delete(expense)
    return True

def update_expense(expense_id,user_id,data):
    get_user_by_id(user_id)

    if not data:
        raise InvalidExpenseException("Required data is missing")
    expense =  __get_validated_expense(expense_id, user_id)

    if "amount" in data:
        if data["amount"] <= 0:
            raise InvalidExpenseException("Amount must be positive")
        expense.amount = data["amount"]
    if "category" in data:
        expense.category = data["category"]

    if "date"  in data:
        expense.date = data["date"]

    return save(expense)


def __validate_expense(data):
    if "amount" not in data or data["amount"] <= 0:
        raise InvalidExpenseException("Amount must be greater than 0")

    if "category" not in data:
        raise InvalidExpenseException("Category is required")

    if "date" not in data:
        raise InvalidExpenseException("Date is required")

def __get_validated_expense(expense_id, user_id):
    expense = get_expenses_by_id(expense_id,user_id)
    if not expense:
        raise ExpenseNotFoundException("No expenses found")
    return expense