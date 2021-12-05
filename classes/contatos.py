from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Contatos (Resource):
    

    def get(self):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

      

        resultado = db.lista_seguindo(usuario['id_user'] )

        lista = []

        for seguindo in resultado:
            item={'id_user': seguindo['id_seguindo']}
            lista.append(item)
        return{'status': 0,  'lista':lista}
   