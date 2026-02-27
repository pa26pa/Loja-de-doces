from flask import Flask, Blueprint,render_template, request, session, make_response
#from auth import connection

views = Blueprint("views", __name__)

@views.route('/', methods=('GET','POST'))
def home():
    return(render_template ('inicio.html'))
#    con = connection()
#    cursor = con.cursor()

