from flask import Flask, render_template, redirect, request, session
import sqlite3 as sql
import os
import re
import datetime


db = sql.connect("F:\\TekNotes\\TekNotes-Blog\\DB\\teknotes.db", check_same_thread=False)
cr = db.cursor()

app_manager = Flask(__name__)

app_manager.config['SECRET_KEY'] = "abcdef12356AAFF"

@app_manager.route("/")
@app_manager.route("/index")
@app_manager.route("/home")
def index():
    try:
        cr.execute("select * from notes ORDER BY id DESC LIMIT 10")
        Data = cr.fetchall()
    except:
        print("Error")
        Data = []
    return render_template("home.html", pagetitle="Home", disableHeader="", data = Data)

@app_manager.route("/contact")
def contact():
    return render_template("contact.html", pagetitle="Contact", disableHeader="none")

@app_manager.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('login'):
        return redirect('admin')

    if request.method == "POST" and request.form["email"] and request.form["password"] :
        email = validate(request.form["email"])
        password = validate(request.form["password"])
        cr.execute("select * from users where email = '"+email+"' and password = '"+password+"' ")
        D = cr.fetchall()
        if(D):
            session['login'] = True
            session['id'] = D[0][0]
            session['name'] = D[0][1]
            session['email'] = D[0][2]
            print(session)
            return redirect('admin')
    return render_template("login.html", pagetitle="Home", disableHeader="none")


@app_manager.route("/admin", methods=['GET'])
def admin():
    if not session.get('login'):
        return redirect('login')

    if request.args.get("id"):
        id = int(validate(request.args.get("id")))
        return render_template("admin.html", pagetitle="Home", disableHeader="none", id = id)

    return render_template("admin.html", pagetitle="Home", disableHeader="none", id=-1)

@app_manager.route("/add", methods=['POST'])
def add():
    if not session.get('login'):
        return redirect('login')

    if request.form["title"] and request.form["content"] and request.form["category"] :
        title = validate(request.form["title"])
        content = validate(request.form["content"])
        category = validate(request.form["category"])
        mydate = datetime.datetime.now()
        noteDate = mydate.strftime("%B %d")
        try:
            cr.execute("insert into notes (title, content, user_id, category, date) values('"+title+"', '"+content+"', 1, '"+category+"', '"+noteDate+"')")
            db.commit()
        except:
            print("Error")
            return  redirect('admin?id=2')

        return redirect('admin?id=1')

    return  redirect('admin?id=2')


def validate(value):
    return re.sub('[^A-Za-z0-9@_$.]+', '', value)

if __name__ == "__main__":
	 app_manager.run()