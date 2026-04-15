from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.expense_service import *

expense_blueprint = Blueprint("expense",__name__)

@expense_blueprint.route("/expense",methods=["POST"])
@jwt_required()
def create():
    user_id= get_jwt_identity()
    data = request.get_json()
    expense = create_expense(data, user_id)

    return jsonify({
        "message": "expense created successfully",
        "expense_id": expense.expense_id
    }),201

@expense_blueprint.route("/expenses", methods=["GET"])
@jwt_required()
def get_all():
    user_id= get_jwt_identity()
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
@jwt_required()
def get_by_category(category):
    user_id = get_jwt_identity()
    expenses = get_expense_by_category(user_id,category)

    return jsonify([
        {
            "id": expense.expense_id,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date.strftime("%Y-%m-%d")
        } for expense in expenses
    ]),200

@expense_blueprint.route("/expenses/date/<date>", methods=["GET"])
@jwt_required()
def get_by_date(date):
    user_id= get_jwt_identity()
    expenses = get_expense_by_date(user_id,date)

    return jsonify([
        {
            "id": expense.expense_id,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date.strftime("%Y-%m-%d")
        } for expense in expenses
    ]),200

@expense_blueprint.route("/expenses/<int:expense_id>", methods=["PATCH"])
@jwt_required()
def update(expense_id):
    data = request.get_json()
    user_id= get_jwt_identity()
    update_expense(expense_id, user_id, data)

    return jsonify({
        "message": "Expense updated"
    }),200

@expense_blueprint.route("/expenses/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense_route(expense_id):
    user_id= get_jwt_identity()
    delete_expense(expense_id, user_id)

    return jsonify({
        "message": "Expense deleted"
    }),200