from database import db
from models.expense import Expense


def save(expense):
    db.session.add(expense)
    db.session.commit()
    return expense

def get_all_expenses_by_user(user_id):
    return Expense.query.filter_by(user_id=user_id).all()

def get_expenses_by_id(expense_id,user_id):
    return Expense.query.filter_by(expense_id=expense_id,user_id=user_id).first()

def get_expenses_by_category(user_id, category):
    return Expense.query.filter_by(user_id=user_id, category=category).all()

def get_expenses_by_date(user_id, date):
    return Expense.query.filter_by(user_id=user_id, date=date).all()

def delete(expense):
    db.session.delete(expense)
    db.session.commit()