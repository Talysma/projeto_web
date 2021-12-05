from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Curtidas (Resource):
    

    def get(self,id_postagem):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

      

        resultado = db.lista_curtidas(id_postagem)

        lista = []

        for curtida in resultado:
            curtidor=db.busca_usuario_id(curtida['id_usuario'])
            item={
                'id_user': curtidor['id_user'],
                'login':curtidor['login']
                }
            lista.append(item)
        return{'status': 0,  'lista':lista}
   