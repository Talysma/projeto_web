from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token



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

