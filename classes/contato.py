from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Contato (Resource):
    def post(self , login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        perfil = db.busca_usuario(login)
        if perfil==None:
            return {'status':2, 'msg': f'Usuário {login} não existe.'}

        resultado = db.seguir(usuario['id_user'] ,perfil['id_user'])

        if resultado==True:
            return {'status': 0, 'msg': f'Passou a seguir {login}.'}
        else:
            return {'status': 1, 'msg': f'Já segue  {login}.'}


    def get(self, login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        perfil = db.busca_usuario(login)
        if perfil==None:
            return {'status':2, 'msg': f'Usuário {login} não existe.'}

        resultado = db.esta_seguindo(usuario['id_user'] ,perfil['id_user'])

        if resultado==None:
            return {'status': 1, 'msg': f'Não está seguindo  {login}.'}

        else:
            return {'status': 0, 'msg': f'Está seguindo  {login}.'}

    def delete(self, login):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}

        perfil = db.busca_usuario(login)
        if perfil==None:
            return {'status':2, 'msg': f'Usuário {login} não existe.'}

        db.desseguir(usuario['id_user'] ,perfil['id_user'])
        return {'status': 0, 'msg': f'Não está  mais  seguindo  {login}.'}

