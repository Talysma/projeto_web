from sys import argv
from flask import request
from flask_restful import Resource
from classes.token import Token
import os


class Foto(Resource):
    def get(self, login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        if os.path.isfile(f"static/img/perfil/{login}"):
            return {'status': 0, 'url':f'{request.host_url}static/img/perfil/{login}'}
        else:
            return {'status': 0, 'url':f'{request.host_url}static/img/imagempadrao.jpg'}



    def post(self, login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))             
        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        if (usuario['login'] != login):
            return {'status': 1, 'msg': 'Você não pode alterar esse perfil.'}
            
        arg = open(os.path.join('static/img/perfil', usuario['login']), 'wb')
        arg.write(request.data)
        arg.close()
        return {'status': 0, 'msg': 'Foto alterada.'}         