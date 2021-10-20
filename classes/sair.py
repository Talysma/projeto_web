from flask import request
from flask_restful import Resource
from classes.token import Token



class Sair(Resource):
    def get(self):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))


        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        Token.apagar_token(request.headers.get ('Authorization'))

        return {'status': 0, 'msg': 'Token encerrado.'}
          

