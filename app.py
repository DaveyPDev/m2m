from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Department, Employee, get_directory

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///employees_db2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/phones')
def list_phones():

    emps = Employee.query.all()
    return render_template('phones.html', emps=emps)

# @app.route('/phones')
# def list_phones():
#     """Renders directory of employees and phone numbers  (from dept)"""
#     emps = Employee.query.all()
#     return render_template('phones.html', emps=emps)
