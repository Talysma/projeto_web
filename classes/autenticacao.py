from flask import request
from flask_restful import Resource
from model import db
from passlib.hash import sha256_crypt
import secrets




class Autenticacao(Resource):
    def get(self, login, senha):
        usuario = db.busca_usuario(login)

        if usuario == None:
            return {'status': 1, 'msg': 'Falha de autenticação.'}

        if sha256_crypt.verify(senha, usuario["senha"]):
            token = secrets.token_hex(128)
            db.adiciona_token(login, token)
            return {'status': 0, 'token': token}
        else:
            return {'status': 1, 'msg': 'Falha de autenticação.'}