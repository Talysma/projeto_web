import sqlite3
from sqlite3.dbapi2 import IntegrityError
from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("model/bancoprincipal.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def busca_usuario(login):
    con = get_db()
    return con.execute("SELECT * FROM usuarios WHERE login = ?",[login]).fetchone()

def busca_usuario_id(id_user):
    con = get_db()
    return con.execute("SELECT * FROM usuarios WHERE id_user = ?",[id_user]).fetchone()


def cadastra_usuario(nome, login, senha):
    con = get_db()
    con.execute("INSERT INTO usuarios VALUES(NULL, ?, ?, ?)", [nome,login, senha])
    con.commit()

def altera_nome(login, nome):
    con = get_db()
    con.execute("UPDATE usuarios SET nome = ? WHERE login = ?",[nome, login])
    con.commit()

def altera_senha(login, senha):
    con = get_db()
    con.execute("UPDATE usuarios SET senha = ? WHERE login = ?", [senha, login])
    con.commit()

def adiciona_token(login, token):
    con = get_db()
    usuario = con.execute("SELECT id_user FROM usuarios WHERE login = ?",[login]).fetchone()
    con.execute("INSERT INTO tokens VALUES(NULL, ?, ?)",[usuario['id_user'], token])
    con.commit()


def verifica_token(token):
    con = get_db()
    dados = con.execute("SELECT * FROM tokens WHERE token = ?",[token]).fetchone()

    if (dados != None):
        return con.execute("SELECT * FROM usuarios WHERE id_user = ?",[dados['id_usuario']]).fetchone()

    else:
        return None

def apaga_token(token):
    con = get_db()
    con.execute("DELETE FROM tokens WHERE token = ?",[token])
    con.commit()



def posta_mensagem(autor , texto):
    con = get_db()
    con.execute("INSERT INTO postagens (de , texto) VALUES( ?, ?)",[autor,texto])
    con.commit()


def lista_mensagens(autor):
    con = get_db()
    return con.execute("SELECT * FROM postagens WHERE de = ? ORDER BY datahora DESC",[autor]).fetchall()


def seguir (seguidor , seguindo):
    try:
        con = get_db()
        con.execute("INSERT INTO seguidores  VALUES(NULl, ?, ?)",[seguidor,seguindo])
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False    

def desseguir (seguidor , seguindo):
    con = get_db()
    con.execute("DELETE FROM seguidores  WHERE id_seguidor = ? AND id_seguindo = ?",[seguidor,seguindo])
    con.commit()

def esta_seguindo(seguidor, seguindo):
    con = get_db()
    return con.execute("SELECT * FROM seguidores  WHERE id_seguidor = ?  AND id_seguindo = ?",[seguidor,seguindo]).fetchone()


def lista_seguindo(seguidor):
     con = get_db()
     return con.execute("SELECT * FROM seguidores  WHERE id_seguidor = ? ",[seguidor]).fetchall()


def curtir(usuario,postagem):
    try:
         con = get_db()
         con.execute("INSERT INTO curtidas  VALUES( NUll,?, ?)",[postagem,usuario])
         con.commit()
         return True
    except sqlite3.IntegrityError:
        return False 


def descurtir(usuario,postagem):
     con = get_db()
     con.execute("DELETE FROM curtidas WHERE id_postagem=? AND id_usuario=?",[postagem,usuario]) 
     con.commit()

def esta_curtindo(usuario,postagem):
    con = get_db()
    return con.execute("SELECT * FROM curtidas WHERE id_postagem=? AND id_usuario=?",[postagem,usuario]) .fetchone()



def pega_postagem(id_postagem):
    con = get_db()
    return con.execute("SELECT * FROM postagens WHERE id_post=? ",[id_postagem]) .fetchone()



def lista_curtidas(id_postagem):
     con = get_db()
     return con.execute("SELECT * FROM curtidas  WHERE id_postagem = ? ",[id_postagem]).fetchall()