from flask import Flask, Blueprint,render_template, request, flash, redirect, url_for, session, make_response
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash 
import pymysql
import random
import smtplib
from email.message import EmailMessage
#from jaja import password
import mimetypes
from backend.resources.auth import signin, login, forgot, redefine_password

app = Flask(__name__)
api = Api(app)

api.add_resource(signin,"/sign")
api.add_resource(login,"/login")
api.add_resource(forgot,"/forgot")
api.add_resource(redefine_password,"/redefine_password")

if __name__ == "__main__":
    app.run(debug=True)
    
