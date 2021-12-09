from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Busca (Resource):
    def get(self , termo):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}


        postagens=db.busca_mensagens(termo)
       
        lista_postagens = []

        for postagem in postagens:
            autor=db.busca_usuario_id(postagem['de'])
            item={
            'id_post':postagem['id_post'],
            'de':postagem['de'],
            'autor':autor['nome'],
            'datahora':postagem['datahora'],
            'texto':postagem['texto']
            }

           
            lista_postagens .append(item)

        usuarios=db.busca_usuarios(termo)
       
        lista_usuarios = []

        for user in usuarios:
            
            item={
            'id_user':user['id_user'],
            'login':user['login'],
            'nome':user['nome'],
            
            }
            lista_usuarios.append(item)

        return{'status': 0,'usuarios':lista_usuarios,'postagens':lista_postagens}
