from model import db


class Token:
    def recebe_token(auth):
        try:
            (tipo, token) = auth.split(' ')
            if tipo.lower() != "bearer":
                return None
            else:
                return token
        except AttributeError:
            return None



    def retorna_usuario(auth):
        token = Token.recebe_token(auth)
        if (token != None):
            return db.verifica_token(token)
        else:
            return None

    def apagar_token(auth):
        token = Token.recebe_token(auth)
        db.apaga_token(token)
