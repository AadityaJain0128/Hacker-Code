from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from encrypt import encrypt
import os
from verify import verify
from db_commands import alter_database, update_solved, fetch_questions, top_problems, fetch_user
from random import randint
from email_otp import send_otp

app = Flask(__name__)
app.config["SECRET_KEY"] = "a"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login-data.db"
db = SQLAlchemy(app)

questions = fetch_questions()

def check_admin():
    if session.get("user") == "aaditya01":
        session["admin"] = True
        return True
    else:
        session["admin"] = False
        return False

def sort_status(user, status):
    questions_ = []
    solved = fetch_user(user)
    for i in questions:
        if str(i[0]) not in solved and "unsolved" in status:
            questions_.append(i)
        if str(i[0]) in solved and "solved" in status:
            questions_.append(i)
    return questions_

def sort_difficulty(questions_, difficulty):
    q = []
    for i in questions_:
        if i[3] in difficulty:
            q.append(i)
    return q


class Login(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    passwd = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    fName = db.Column(db.String(30), nullable=False)
    lName = db.Column(db.String(30), nullable=False)
    completed = db.Column(db.String(1000))


@app.route("/", methods=['GET', 'POST'])
def home():
    user = session.get("user")
    check_admin()
    if not(user):
        session.clear()
        return redirect("/log-in")

    data = Login.query.filter_by(username=user).first()
    if request.method == "POST":
        if request.form.get("log-out"):
            session.pop("user", None)
            return redirect("/log-in")
        else:
            unsolved = request.form.get("unsolved")
            solved = request.form.get("solved")
            easy = request.form.get("easy")
            medium = request.form.get("medium")
            hard = request.form.get("hard")

            s1 = s2 = d1 = d2 = d3 = ""
            if not (unsolved or solved or easy or medium or hard):
                return render_template("index.html", data=data, questions=questions)

            if unsolved:
                s1 = "checked"
            if solved:
                s2 = "checked"
            if easy:
                d1 = "checked"
            if medium:
                d2 = "checked"
            if hard:
                d3 = "checked"
            if (unsolved or solved) and (easy or medium or hard):
                questions_ = sort_difficulty(sort_status(user, [unsolved, solved]), [easy, medium, hard])
            elif unsolved or solved:
                questions_ = sort_status(user, [unsolved, solved])
            elif easy or medium or hard:
                questions_ = sort_difficulty(questions, [easy, medium, hard])
            return render_template("index.html", data=data, questions=questions_, s1=s1, s2=s2, d1=d1, d2=d2, d3=d3)
    return render_template("index.html", data=data, questions=questions)


@app.route("/log-in", methods=['GET', 'POST'])
def login():
    user = session.get("user")
    check_admin()
    if user:
        return redirect("/")
    if request.method == "POST":
        user_check = email_check = ""
        if request.form["select"] == "username_select":
            user = request.form["username"]
            val = user
            user_check = "checked"
            data = Login.query.filter_by(username=user).first()
        elif request.form["select"] == "email_select":
            email = request.form["email"]
            val = email
            email_check = "checked"
            data = Login.query.filter_by(email=email).first()
        passwd = encrypt(request.form["passwd"])
        if data != None:
            if passwd == data.passwd:
                user = data.username
                session["user"] = user
                return redirect("/")
            return render_template("log-in.html", err="Password is Incorrect !", val=val, user_check=user_check, email_check=email_check)
        return render_template("log-in.html", err="This UserName / E-Mail ID does not exist !", val=val, user_check=user_check, email_check=email_check)
    return render_template("log-in.html", user_check="checked")


@app.route("/sign-up", methods=['GET', 'POST'])
def signup():
    user = session.get("user")
    if user:
        return redirect("/")
    if request.method == "POST":
        fName = request.form.get("fName")
        lName = request.form.get("lName")
        username = request.form.get("username")
        email = request.form.get("email")
        passwd = encrypt(request.form.get("passwd"))

        if Login.query.filter_by(username=username).first():
            return render_template("sign-up.html", err="This UserName is Not Available", fName=fName, lName=lName, email=email, username=username)
        data = Login(fName=fName, lName=lName, username=username, email=email, passwd=passwd)
        db.session.add(data)
        db.session.commit()
        if username not in os.listdir("static/users"):
            os.makedirs(f"static/users/{username}")
        return redirect("/log-in")
    return render_template("sign-up.html")


@app.route("/problem/<int:qno>", methods=['GET', 'POST'])
def problem(qno):
    check_admin()
    if request.method == "POST":
        user = session.get("user")
        if not(user):
            q = questions[qno - 1]
            return render_template("/problem.html", q=q)
        script = request.form.get("script")
        with open(f"static/users/{user}/problem_{qno}.txt", "w") as f:
            f.writelines(script.split("\n"))
        q = questions[qno - 1]
        success, msg, colour = verify(qno, user)

        d = Login.query.filter_by(username=user).first()
        if success:
            if d.completed != None:
                completed = d.completed
                if str(qno) not in completed.split(","):
                    completed += f"{qno},"
            else:
                completed = f"{qno},"
            Login.query.filter_by(username=user).update({Login.completed : completed})
        else:
            if d.completed != None:
                completed = d.completed.split(",")
                if str(qno) in completed:
                    completed.remove(str(qno))
                    completed = ",".join(completed)
                    if completed == "":
                        Login.query.filter_by(username=user).update({Login.completed : None})
                    else:
                        Login.query.filter_by(username=user).update({Login.completed : completed})

        db.session.commit()
        update_solved(qno)
        return render_template("/problem.html", q=q, msg=msg, colour=colour, script=script)

    if 1 <= qno <= len(questions):
        q = questions[qno - 1]
        user = session.get("user")
        if user:
            path = f"problem_{qno}.txt"
            if path in os.listdir(f"static/users/{user}"):
                with open(f"static/users/{user}/{path}") as f:
                    script = f.read()
                return render_template("problem.html", q=q, script=script)
        return render_template("problem.html", q=q)
    return redirect("/")


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    check_admin()
    user = session.get("user")
    if not(user):
        return redirect("/log-in")

    d = Login.query.filter_by(username=user).first()
    n = 0
    if d.completed != None:
        n = len(d.completed.split(",")[:-1])
    return render_template("profile.html", d=d, n=n)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if not check_admin():
        return redirect("/")
    if request.method == "POST":
        # if request.form.get("questions_btn") and not request.form.get("login_btn"):
        qno = request.form.get("qno")
        title = request.form.get("title")
        desc = request.form.get("desc")
        difficulty = request.form.get("difficulty")
        result = alter_database(qno, title, desc, difficulty)
        return render_template("admin.html", qno=qno, title=title, desc=desc, result=result)
        # else:
            # username = request.form.get("username")
            # result = alter_database("login-data", [username])
            # return render_template("admin.html", username=username, result=result)
    return render_template("admin.html")


@app.route("/top-problems", methods=['GET', 'POST'])
def topproblems():
    user = session.get("user")
    check_admin()
    data = Login.query.filter_by(username=user).first()
    top_q = top_problems()
    return render_template("top-problems.html", top_q=top_q, data=data)


@app.route("/log-in/forgot-password", methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        password = request.form.get("password", None)
        if password:
            email = session.get("email")
            Login.query.filter_by(email=email).update({Login.passwd : encrypt(password)})
            db.session.commit()
            session.clear()
            return render_template("forgot.html", ver=True, msg="Password Changed Successfully.")

        email = request.form.get("email")
        data = Login.query.filter_by(email=email).first()
        otp = session.get("otp", None)
        if otp:
            _ = request.form.get("otp")
            if _ == otp:
                session.pop("otp", None)
                return render_template("forgot.html", colour="green", ver=True)
            return render_template("forgot.html", msg="Incorrect OTP", colour="red", email=email, otp=_)
        if not data:
            return render_template("forgot.html", msg="This Email ID is not registered with us.", colour="red", email=email, display_otp="none")
        otp = str(randint(1000, 9999))
        session["otp"] = otp
        if not send_otp(email, otp):
            return render_template("forgot.html", msg="Error Occured while sending OTP.", colour="red", email=email, display_otp="none")
        session["email"] = email
        return render_template("forgot.html", msg="OTP sent successfully.", colour="green", email=email, display_otp="block")
    return render_template("forgot.html", display_otp="none")

if __name__ == "__main__":
    app.run(debug=True)