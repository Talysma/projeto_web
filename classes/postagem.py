from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Postagem (Resource):
    def get(self):
        pass
        
    def post(self):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}


        try:
            texto = request.form['texto']
            if texto == '':
                return {'status': 2, 'msg': 'Não pode texto em branco.'}
            db.posta_mensagem(usuario['id_user'],texto)
            return {'status': 0, 'msg': 'Mensagem postada.'}
                              
        except KeyError:
            return {'status':1, 'msg': 'Falta informar o texto.'}

       