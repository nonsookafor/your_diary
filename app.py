from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'



db = SQLAlchemy(app)
admin = Admin(app)
app.secret_key = "secret_key"



class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    date = db.Column(db.DateTime, default = datetime.now(), nullable = True)

    def __init__(self, email, password, date):
        self.email = email
        self.password = password
        self.date = date

    def __repr__(self):
        return U'<Users%r' % self.email
admin.add_view(ModelView(Users, db.session))



class Their_Diaries(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80))
    date = db.Column(db.DateTime, default = datetime.now(), nullable = True)
    diary = db.Column(db.String(254), default = "", nullable = True)

    def __init__(self, email, date, diary):
        self.email = email
        self.date = date
        self.diary = diary

    def __repr__(self):
        return U'<Their_Diaries%r' % self.email
admin.add_view(ModelView(Their_Diaries, db.session))



@app.route("/", methods = ["POST", "GET"])
def index():
    if "email" in session:
        session.pop("email", None)
    return render_template("index.html")



@app.route("/home/", methods = ["POST", "GET"])
def home():
    if request.method == "GET":
        if "email" in session:
            return render_template("home.html")
        else:
            return redirect(url_for("signin"))
    else:
        diary = request.form['diary']
        the_diary = diary
        if "email" in session:
            email = session["email"]
            user = Their_Diaries(email=email, date=datetime.now(), diary=the_diary)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return redirect(url_for("signin"))



@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form['email']
        password = request.form['password']
        user = Users(email=email, password=password, date = datetime.now())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("signin"))



@app.route("/signin", methods = ["POST", "GET"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        email = request.form['email']
        password = request.form['password']
        if Users.query.filter_by(email = email).count() > 0:
            signed = Users.query.filter_by(email=email).first()
            print(signed)
            if signed.password == password:
                session["email"] = email
                return redirect(url_for('home'))
            else:
                return redirect(url_for("signup"))
        else:
            return redirect(url_for("signup"))



@app.route("/records", methods = ["GET"])
def records():
    if "email" in session:
        email = session["email"]
        if Their_Diaries.query.filter_by(email = email).count() > 0:
            signed = Their_Diaries.query.filter_by(email = email).all()
            print("\n\n\n\n", signed)
            return render_template("records.html", names=signed, the_email=email)
        else:
            return redirect(url_for("home.html"))
    else:
        return redirect(url_for("signin"))




        


if __name__ == "__main__":
    app.run(debug = True)