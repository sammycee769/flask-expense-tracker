from flask import Blueprint, request, jsonify

from services.authentication_service import token_required
from services.expense_service import *

expense_blueprint = Blueprint("expense",__name__)

@expense_blueprint.route("/expense",methods=["POST"])
@token_required
def create(user_id):
    data = request.get_json()
    expense = create_expense(data, user_id)

    return jsonify({
        "message": "expense created successfully",
        "expense_id": expense.expense_id
    }),201

@expense_blueprint.route("/expenses", methods=["GET"])
@token_required
def get_all(user_id):
    expenses = fetch_all_expenses(user_id)

    return jsonify([
        {
            "id": expense.expense_id,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date.strftime("%Y-%m-%d")
        } for expense in expenses
    ]),200

@expense_blueprint.route("/expenses/category/<category>", methods=["GET"])
@token_required
def get_by_category(user_id,category):
    expenses = get_expenses_by_category(user_id,category)

    return jsonify([
        {
            "id": expense.expense_id,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date.strftime("%Y-%m-%d")
        } for expense in expenses
    ]),200

@expense_blueprint.route("/expenses/date/<date>", methods=["GET"])
@token_required
def get_by_date(user_id,date):
    expenses = get_expenses_by_date(user_id,date)

    return jsonify([
        {
            "id": expense.expense_id,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date.strftime("%Y-%m-%d")
        } for expense in expenses
    ]),200

@expense_blueprint.route("/expenses/<int:expense_id>", methods=["PATCH"])
@token_required
def update(expense_id, user_id):
    data = request.get_json()
    update_expense(expense_id, user_id, data)

    return jsonify({
        "message": "Expense updated"
    }),200

@expense_blueprint.route("/expenses/<int:expense_id>", methods=["DELETE"])
@token_required
def delete_expense_route(expense_id, user_id):
    delete_expense(expense_id, user_id)

    return jsonify({
        "message": "Expense deleted"
    }),200