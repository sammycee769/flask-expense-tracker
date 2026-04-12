from flask import Flask
from flask import jsonify
from flask_restx import Api

from exceptions.expense_exceptions import *
from exceptions.user_exceptions import *
from database import init_db
from routes.expense_routes import expense_blueprint
from routes.user_routes import user_blueprint

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title="ExpenseTracker Api",
          description="an api that helps users track their expenses"
          )

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:christian@localhost/expense_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "a_very_long_random_secret_key_769085"


init_db(app)

app.register_blueprint(user_blueprint, url_prefix="/api/users")
app.register_blueprint(expense_blueprint, url_prefix="/api")

@app.errorhandler(InvalidCredentialsException)
def handle_invalid_credentials(e):
    return jsonify({
        "error": str(e)
    }), 401


@app.errorhandler(UserAlreadyExistsException)
def handle_user_exists(e):
    return jsonify({
        "error": str(e)
    }), 400


@app.errorhandler(UserNotFoundException)
def handle_user_not_found(e):
    return jsonify({
        "error": str(e)
    }), 404

@app.errorhandler(Exception)
def handle_general_exception(e):
    return jsonify({
        "error": "Something went wrong",
        "details": str(e)
    }), 500

@app.errorhandler(ExpenseNotFoundException)
def handle_expense_not_found(e):
    return jsonify({
        "error": str(e)
    }), 404


@app.errorhandler(UnAuthorizedUserException)
def handle_unauthorized_expense(e):
    return jsonify({
        "error": str(e)
    }), 403


@app.errorhandler(InvalidExpenseException)
def handle_invalid_expense(e):
    return jsonify({
        "error": str(e)
    }), 400


if __name__ == "__main__":
    app.run(debug=True)
