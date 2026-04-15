from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.user_service import *

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/register",methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    user = register_user(data)

    return jsonify({
        "message": "User registered successfully",
        "user": user.user_id
    }),201

@user_blueprint.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    token = login_user(data)

    return jsonify({
        "token": token,
        "message": "User logged in"
    }),200

@user_blueprint.route("/me",methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = get_user(user_id)

    return jsonify({
        "id": user.user_id,
        "username": user.username,
        "email": user.email,
    })

@user_blueprint.route("/me",methods=["PATCH"])
@jwt_required()
def update():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    user = update_user(user_id,data)

    return jsonify({
        "message": "User updated successfully",
        "user": user.user_id
    })

@user_blueprint.route("/me",methods=["DELETE"])
@jwt_required()
def delete():
    user_id = get_jwt_identity()
    delete_user(user_id)

    return jsonify({
        "message": "User deleted successfully",
    })