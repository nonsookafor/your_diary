from flask import Flask, render_template, request, url_for, redirect
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



class Signed(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    date = db.Column(db.DateTime, default = datetime.now(), nullable = True)

    def __init__(self, email, password, date):
        self.email = email
        self.password = password
        self.date = date

    def __repr__(self):
        return U'<Signed%r' % self.email
admin.add_view(ModelView(Signed, db.session))



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80))
    date = db.Column(db.DateTime, default = datetime.now(), nullable = True)
    diary = db.Column(db.String(254), default = "", nullable = True)

    def __init__(self, email, date, diary):
        self.email = email
        self.date = date
        self.diary = diary

    def __repr__(self):
        return U'<User%r' % self.email
admin.add_view(ModelView(User, db.session))



@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("index.html")



@app.route("/home/<email>", methods = ["POST", "GET"])
def home(email):
    if request.method == "GET":
        return render_template("home.html")
    else:
        diary = request.form['diary']
        the_diary = diary
        user = User(email=email, date=datetime.now(), diary=the_diary)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home', email=email))



@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form['email']
        password = request.form['password']
        user = Signed(email=email, password=password, date = datetime.now())
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
        if Signed.query.filter_by(email = email).count() > 0:
            signed = Signed.query.filter_by(email=email).first()
            print(signed)
            if signed.password == password:
                print('\n\n\n\n\n', email, '\n', password)
                return redirect(url_for('home', email=email))
            else:
                return redirect(url_for("signup"))
        else:
            return redirect(url_for("signup"))



@app.route("/records")
def records():
    return render_template("records.html")


        


if __name__ == "__main__":
    app.run(debug = True)