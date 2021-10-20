
from flask import request
from flask_restful import Resource
from model import db
from passlib.hash import sha256_crypt

class Cadastro(Resource):
    def post(self):    
        try:
            if (request.form["nome"] == "" or
                request.form["login"] == "" or
                request.form["senha1"] == "" or
                request.form["senha2"] == ""  ):
                return {'status': 3, 'msg': 'Todos os campos precisam ser preenchidos.'}
        
            usuario = db.busca_usuario(request.form["login"])
            if usuario == None:
                if request.form["senha1"] == request.form["senha2"]:
                    senha_hash = sha256_crypt.hash(request.form["senha1"])
                    db.cadastra_usuario(request.form["nome"],request.form["login"], senha_hash)
                    return {'status': 0, 'msg': 'Cadastro efetuado.'}
                else:
                    return {'status': 1, 'msg': 'As senhas não coincidem.'}
            else:
                return {'status': 2, 'msg': 'Esse usuário já existe.'}                     
        except KeyError:
            return {'status': -1, 'msg': 'Faltam parâmetros.'} 