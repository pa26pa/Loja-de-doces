from flask import Flask, Blueprint,render_template, request, flash, redirect, url_for, session, make_response
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash 
import pymysql
import random
import smtplib
from email.message import EmailMessage
#from jaja import password
import mimetypes
from auth import signin

app = Flask(__name__)
api = Api(app)

api.add_resource(signin,"/sign")

if __name__ == "__main__":
    app.run(debug=True)
    
