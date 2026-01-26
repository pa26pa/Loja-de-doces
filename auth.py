from flask import Flask, Blueprint,render_template, request, flash, redirect, url_for, session 
from werkzeug.security import generate_password_hash, check_password_hash 
import pymysql
import random
import smtplib
from email.message import EmailMessage
from jaja import password
import mimetypes


auth = Blueprint('auth', __name__)

# conexão com o my sql
def connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Pg260410',
        database='mania doce',
        cursorclass=pymysql.cursors.Cursor 
    )

# criação do sign-up
@auth.route('/sign-up', methods=["GET","POST"])
def sign():
    if request.method == "POST":
        nome = request.form.get('nome')
        CPF = request.form.get('cpf')
        email = request.form.get('email')
        telefone = request.form.get('tel')
        data_de_nascimento =  request.form.get('date')
        senha = request.form.get('password')
        
        #chamando conexão
        con = connection()
        cursor = con.cursor()
        
        #checando se já existe uma conta
        
        query = """select CPF,email, telefone from usuarios where CPF = %s or email = %s or telefone = %s"""
        cursor.execute(query,(CPF,email,telefone))
        existe = cursor.fetchone()
        
        senha_lock = generate_password_hash(senha)
        
        if existe:
            flash('Já existe uma conta com este CPF, email, ou telefone', category='error')
            cursor.close()
            con.close()
            return render_template('inicio.html')
        else:
            flash('Cadastro feito com sucesso', category='success')
            
            cria = """insert into usuarios (CPF, nome, email, telefone, data_de_nascimento, senha) values (%s,%s,%s,%s,%s,%s)"""
            cursor.execute(cria,(CPF,nome,email,telefone,data_de_nascimento,senha_lock))
            con.commit()
            cursor.close()
            con.close()
            return render_template('inicio.html')

    return render_template('cadastro.html')

# criação do login
@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        CPF = request.form.get('cpf')
        senha = request.form.get('senha')
        
        con = connection()
        cursor = con.cursor()
        
        senha_hash = generate_password_hash(senha)
        
        #procurando se já existe o cadastro
        search = """select CPF from usuarios where CPF = %s"""
        cursor.execute(search,(CPF))
        search_true = cursor.fetchone()
        
        if search_true and check_password_hash(search_true[0],senha_hash):
            flash('Você está logado', category='success')
           
            cursor.close()
            con.close()
            return render_template('home.html')
        else:
           
            cursor.close()
            con.close()
            flash('Senha incorreta', category='error')
            return redirect(url_for('auth.sign'))
    
    return render_template('inicio.html')

#criação do esqueci minha senha
@auth.route('/forgot', methods=["GET","POST"])
def forgot():
    #definindo que o metodo será POST :)
   if request.method == "GET":
       return render_template('home.html')
   
    # se for mandado o CPF
   if 'cpf' in request.form:
       CPF = request.form.get('cpf')
       
       con = connection()
       cursor = con.cursor()
       
      #Checando se o usuário existe
       query = """select CPF from usuarios where CPF = %s"""
       cursor.execute(query,(CPF))
       usuario = cursor.fetchone()
       
       
       if not usuario:
         cursor.close()
         con.close()
         flash('Não há conta com este CPF, por favor cadastre-se', category='error')
         return redirect(url_for('auth.sign'))   
        
       #procurando o email correspondente
       q = """select email from usuarios where CPF = %s"""
       cursor.execute(q,(CPF,))
       email = cursor.fetchone()
             
              
       flash('Mandamos um código no seu email, por favor insira ele no espaço abaixo', category="success")
                
       code = random.randint(100000,999999)
                
       session['code'] = str(code) 
       session['cpf'] = CPF
                
       #mandando o email       
       FROM = 'paula.pires2640@gmail.com'
       info = 'Mania Doce / esqueci senha'
         
       to = email[0]
                
       msg = EmailMessage()
       msg['From'] = FROM
       msg['To'] = to
       msg['Subject'] = info
       msg.set_content(f'Olá, aqui está o seu código: {code}')
       
       with smtplib.SMTP_SSL("smtp.gmail.com",465) as email:
           email.login(FROM,password)
           email.send_message(msg)
           return render_template('code.html')
    
    #se o codigo for mandado        
   if 'codigo' in request.form:
                
       codigo = request.form.get('codigo')
       senha = request.form.get('nova_senha')
            
     
                     
       if  codigo != session.get('code'):
          flash('Código errado', category='error')
          return render_template('home.html')
 
       con = connection()
       cursor = con.cursor()
       senha_nova = generate_password_hash(senha)
       nova = """update usuarios set senha = %s  where CPF = %s"""
       cursor.execute(nova,(senha_nova, session.get('cpf')))
                            
                            
       con.commit() 
       cursor.close()
       con.close()
       flash('senha mudada com sucesso', category="success")
       return render_template('home.html')
                            
    
    


#fim do códigoooo yeyyyyyyyyyyyyyyyyyyyyyy