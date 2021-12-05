from flask import request
from flask_restful import Resource
from model import db
from classes.token import Token
from passlib.hash import sha256_crypt



class Feed (Resource):

    def pega_postagens(id_user):
        postagens = db.lista_mensagens(id_user)
        
        seguindo=db.lista_seguindo(id_user)
        for perfil in seguindo:
            postagens=postagens +(db.lista_mensagens(perfil['id_seguindo']))

        lista=[] 
        for postagem in postagens:
            autor=db.busca_usuario_id(postagem["de"])
          

            item={
                "id_post":postagem["id_post"],
                "autor":autor["nome"],
                "autor_login":autor["login"],
                "datahora":postagem["datahora"],
                "texto":postagem["texto"]
                
                }
            lista.append(item)

        lista=sorted(lista,key=lambda item:item['datahora'],reverse=True ) 
        return lista 




    def get(self ):
        usuario = Token.retorna_usuario(request.headers.get ('Authorization'))

        if (usuario == None):
            return {'status': -1, 'msg': 'Token inválido.'}
        
        lista=Feed.pega_postagens(usuario['id_user']) 


        for item in lista:
            resultado = db.esta_curtindo(usuario['id_user'],item['id_post'])
            if resultado == None:
                item['curtiu'] = False
            else:
                item['curtiu'] = True


            resultado = db.lista_curtidas(item['id_post'])
            item['curtidas'] = len(resultado)


        return{'status': 0,  'lista':lista}