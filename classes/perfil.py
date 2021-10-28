from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Perfil(Resource):
    def get(self, login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        perfil = db.busca_usuario(login)
        if (perfil == None):
            return {'status': 1, 'msg': 'Perfil não encontrado.'}

        else:
            return {'status': 0, 'login': login, 'nome': perfil['nome']}

    def post(self, login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        alterou_nome = True
        alterou_senha= True


        if (usuario['login']!=login):
            return {'status': 2, 'msg': 'Você  não pode alterar esse perfil.'}



        try:
            db.altera_nome(login, request.form["nome"])              
        except KeyError:
            alterou_nome = False


        try:
            if(request.form["senha1"] != request.form["senha2"]):
                return  {'status': 1, 'msg': 'As senhas não coincidem.'}

            if (request.form["senha1"] ==''):
                return  {'status': 0, 'msg': 'A senha foi mantida.'}
            senha_hash = sha256_crypt.hash(request.form["senha1"])                  
            db.altera_senha(login, senha_hash)                   
        except KeyError:
            alterou_senha = False

        if (alterou_senha or alterou_nome):
            return  {'status': 0, 'msg': 'Perfil alterado.'}
        else:
            return  {'status': 3, 'msg': 'Perfil  não alterado.'}
