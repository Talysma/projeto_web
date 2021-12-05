from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Curtida(Resource):
    def post(self , id_postagem):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        
        postagem=db.pega_postagem(id_postagem)
        if postagem==None:
            return {'status': 2, 'msg': f'Postagem não existe.'}



        resultado = db.curtir(usuario['id_user'] ,id_postagem)

        if resultado==True:
            return {'status': 0, 'msg': f'Postagem curtida.'}
        else:
            return {'status': 1, 'msg': f'Postagem já estava curtida .'}


    def get(self, id_postagem):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

     

        resultado = db.esta_curtindo(usuario['id_user'],id_postagem)

        if resultado==None:
            return {'status': 1, 'msg': f'Não está curtindo esta postagem.'}

        else:
            return {'status': 0, 'msg': f'Está curtindo esta postagem.'}




    def delete(self, id_postagem):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        
        db.descurtir(usuario['id_user'] ,id_postagem)
        return {'status': 0, 'msg': f'Não está  mais  curindo esta postagem.'}

