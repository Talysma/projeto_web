from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt
from datetime import datetime


class Postagens (Resource):
    def get(self , login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        perfil = db.busca_usuario(login)

        if perfil==None:
            return{'status': 2, 'msg': 'O perfil não existe.'}

        postagens = db.lista_mensagens(perfil['id_user'])
        lista = []

        for postagem in postagens:
            item={'datahora':postagem['datahora'],'texto':postagem['texto']}
            lista.append(item)
        return{'status': 0,  'lista':lista}








