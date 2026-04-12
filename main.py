from flask import Flask

from database import init_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:christian@localhost/expense_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)
app.register_blueprint()

if __name__ == "__main__":
    app.run(debug=True)
