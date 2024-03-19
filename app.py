# Python Flask Application development
# Creating a project and virtual environment using visual studio code and installing the required packages

# Import required packages

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
)  # pip install flask
from flask_sqlalchemy import SQLAlchemy  # pip install flask_sqlalchemy
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

pymysql.install_as_MySQLdb()

# Initialize the app
app = Flask(__name__, template_folder="templates")
app.secret_key = "super secret key"

ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql://root:1504mysqlrp7%40%23@localhost:3306/loan_approval_pred"
    )
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql://root:1504mysqlrp7%40%23@localhost:3306/loan_approval_pred"
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["username"] = username
            return redirect(url_for("enter_details"))
        else:
            return "Invalid username or password"
    return render_template("login.html")


@app.route("/enter_details", methods=["GET", "POST"])
def enter_details():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "username" not in session:
        return redirect(url_for("login"))
    # Implement your prediction logic here
    return render_template("prediction_results.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
