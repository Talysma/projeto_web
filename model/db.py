import sqlite3
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
