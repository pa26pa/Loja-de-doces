from flask import Flask, Blueprint,render_template, request, flash, redirect, url_for, session, make_response
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash 
import pymysql
import random
import smtplib
from email.message import EmailMessage
#from jaja import password
import mimetypes
from backend.database.sql import conection

class signin(Resource):
    def post(self):
        data = request.get_json()
        
        con = conection()
        cursor = con.cursor()
        
        cpf = data.get("CPF")
        nome = data.get("nome")
        email = data.get("email")
        telefone = data.get("telefone")
        endereço = data.get("endereço")
        data_de_nascimento = data.get("data_de_nascimento")
        senha = data.get('senha')
        
        senha_hash = generate_password_hash(senha)
        
        query = """select * from usuarios where CPF = %s or email = %s or telefone = %s"""  
        cursor.execute(query,(cpf, email, telefone))      
        
        existe = cursor.fetchone()
        
        if existe:
            return{
                "status":"error",
                "erro":"Já existe um usuario"
                }, 400
        
        
        insert = """insert into usuarios(CPF,nome,email,telefone,endereço,data_de_nascimento,senha) values (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert,(cpf,nome,email,telefone,endereço,data_de_nascimento,senha_hash))
            
        con.commit()
        
        cursor.close()
        con.close()
        return{
            'status':'success',
            'mensagem':'Seu cadastro foi executado com sucesso'
            }, 200
        
    def get(self):
        return {
            'status':'error',
            "erro":"GET não é permitido"
            }, 400

class login(Resource):
    def post(self):
        con = conection()
        cursor = con.cursor()
        data = request.get_json()
        
        email = data.get('email')
        senha = data.get('senha')
        
        search = """select * from usuarios where email = %s"""
        cursor.execute(search,(email,))
        login_valido = cursor.fetchone() 
        
        if login_valido and check_password_hash(login_valido['senha'], senha):
            session['usuario_id'] = login_valido['id_usuario']
            return {
                'status':'success',
                'mensagem':"Login feito com sucesso"
                }, 200
        
        
        return {
            'status':'error',
            "erro":"CPF ou senha incorretos"
            }, 400
        
    def get(self):
        return {
            'status':'error',
            "erro":"GET não é permitido"}, 400
    

class forgot(Resource):
    def post(self):
        con = conection()
        cursor = con.cursor()
        data = request.get_json()
        
        cpf = data.get('CPF')
        
        look = """select * from usuarios where CPF = %s"""
        cursor.execute(look,(cpf,))
        found = cursor.fetchone()
        
        if not found:
            cursor.close()
            con.close()
            return{
                "status":'error',
                "erro":'Não existe um usuario com este CPF'
                }, 400
        
        q = """select email from usuarios where CPF = %s"""
        cursor.execute(q,(cpf,))
        user_email = cursor.fetchone()
        
        code = random.randint(100000,999999)
        
        session["code"] = str(code)
        session["cpf"] = cpf
        
        
        _from = 'paula.pires2640@gmail.com'
        to = user_email[0]
        password = 'rvcr wtfd gtal ijog'
        
        info = 'Mania Doce | esqueceu a senha'
        
        msg = EmailMessage()
        msg['From'] = _from
        msg['To'] = to
        msg['Subject'] = info
        msg.set_content(f'Olá, aqui está o seu código: {code}')
        
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as email:
            email.login(_from,password)
            email.send_message(msg)
        
        return{
            'status':'success',
            'mensagem':'Um código foi enviado no seu email'}, 200
    
    def get(self):
        return {
            'status':'error',
            "erro":"GET não é permitido"}, 400

class redefine_password(Resource):
    def post(self):
        con = conection()
        cursor = con.cursor()
        data = request.get_json()
        
        codigo = data.get('codigo')
        nova_senha = data.get('nova_senha')
        
        nova_senha_hash = generate_password_hash(nova_senha)
        
        if codigo != session.get("code"):
            return {
                'status':'error',
                'erro':'Código incorreto'
                }, 400
        
        update = """update usuarios set senha = %s where id_usuario = %s """
        cursor.execute(update,(nova_senha_hash,session['usuario_id']))
        con.commit()
        
        cursor.close()
        con.close()
        
        return{
            'status':'success',
            'mensagem':'Senha mudada com sucesso'}, 200
            
    def get(self):
        return {
            'status':'error',
            'erro':'GET não é permitido'
                }, 400
    
class add_to_cart(Resource):
    def post(self):
        con = conection()
        cursor = con.cursor()
        data = request.get_json()
        
        id_produto = data.get('id_produto')
        quantidade = data.get('quantidade')
        
        reserved = """select quantidade from produtos where id_produto = %s"""
        cursor.execute(reserved,(id_produto,))
        estoque = cursor.fetchone()
        
        if estoque < quantidade:
            return{
                'status':'error',
                'mensagem':'Só temos {estoque} itens disponiveis'
            }, 400
        
        if 'carrinho' not in session:
            session['carrinho'] = {}
            session['carrinho'][id_produto] = quantidade
        
        elif id_produto in session['carrinho']:
            session['carrinho'][id_produto] += quantidade
        
        else:
            session['carrinho'][id_produto] = quantidade

        return{
            'status':'success',
            'mensagem':'Produto adicionado no carrinho'
            }, 200
    
    def get(self):
        return{
            'status':'error',
            'mensagem':'GET não é permitido'
        }, 400
    