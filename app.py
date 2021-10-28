
#Talysma,Ana Sales,Ravena,Maria Luiza#


from flask import Flask, redirect, url_for, session,request,render_template,jsonify
from flask_restful import Api
from model import db
import os
import secrets
from passlib.hash import sha256_crypt


from classes.cadastro import Cadastro
from classes.autenticacao import Autenticacao
from classes.perfil import Perfil
from classes.sair import Sair
from classes.foto import Foto


app = Flask(__name__)
api = Api(app)

api.add_resource(Cadastro, '/api/cadastro')
api.add_resource(Autenticacao, '/api/autenticacao/<login>/<senha>')
api.add_resource(Perfil, '/api/perfil/<login>')
api.add_resource(Sair, '/api/sair')
api.add_resource(Foto, '/api/foto/<login>')



app.secret_key = b'kljHI@gilds][s-39SIHD;.,&s'

app.config['PERFIL_FOLDER'] = 'static/img/perfil'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1000
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()  in ALLOWED_EXTENSIONS
 

@app.route("/")
def index():
    if "usuario" in session: 
        return render_template("index.html", login = session['usuario'])
    else:
        return render_template("login.html")

@app.route("/autenticacao/<login>/<senha>")
def autenticacao_web(login, senha):
    usuario = db.busca_usuario(login)

    if sha256_crypt.verify(senha, usuario["senha"]):
        session["usuario"] = login
        session["nome"] = usuario["nome"]
        return redirect(url_for("index"))
    else:
        return f"Erro de autenticação."

@app.route("/sair") 
def sair_web():
    del(session["usuario"])
    del(session["nome"])
    return redirect(url_for("index"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro_web():
    
    if request.method == "POST":
        usuario = db.busca_usuario(request.form["login"])
        if usuario == None:                
            if request.form["senha1"]== request.form["senha2"]:
                senha_hash = sha256_crypt.hash(request.form["senha1"])
                db.cadastra_usuario(request.form["nome"],request.form["login"], senha_hash)
                return render_template("usuariocadastrado.html")

            else:
                return render_template("senha.html") 
        else:
            return render_template("usuarioexistente.html") 
                                    
    else:
        return render_template("cadastro.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("index"))
    else:
        if request.method == "POST":
            usuario = db.busca_usuario(request.form["login"])

            if sha256_crypt.verify(request.form["senha"],usuario["senha"]):
                session["usuario"] = request.form["login"]
                session["nome"]  = usuario["nome"]  
                return redirect (url_for("index"))

            else:                                   
                return render_template("erroautenticacao.html")
        else:         
            return render_template("login.html")


@app.route("/perfil/<login>")
def perfil_web(login):
    usuario = db.busca_usuario(login)
    if usuario == None:
        return render_template("perfilnencontrado.html")
    else:
        return render_template("perfil.html", usuario=usuario, eu=session["usuario"])



@app.route("/perfil", methods=["GET", "POST"])
def perfil_edicao():
    if request.method == "POST":
        if request.form["senha1"] != "":
            if request.form["senha1"] != request.form["senha2"]:
                return render_template("senhae.html") 
            else:
                senha_hash = sha256_crypt.hash(request.form["senha1"])
                db.altera_senha(session["usuario"], senha_hash)
        db.altera_nome(session["usuario"], request.form["nome"])
        session["nome"]= request.form["nome"]
        return redirect(url_for('index'))
    else:
        return render_template("editar.html", nome=session["nome"], login=session["usuario"])


@app.route('/perfil/avatar/<login>')
def perfil_avatar(login):

    if os.path.isfile(f"{app.config['PERFIL_FOLDER']}/{login}"):
        return redirect(f"/{app.config['PERFIL_FOLDER']}/{login}")

    else:
        return redirect("/static/img/imagempadrao.jpg")


@app.route('/perfil/foto', methods=["POST"])
def perfil_foto():
    if "foto" not in request.files:
        return "Nenhum arquivo enviado."

    arquivo = request.files["foto"]
    if arquivo.filename == '':
        return "Nenhum arquivo selecionado."

    if arquivo_permitido(arquivo.filename):
        arquivo.save(os.path.join(app.config['PERFIL_FOLDER'],session["usuario"]))
        return redirect(url_for('index'))
    else:
        return render_template ("arquivoinvalido.html")

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template ("arquivogrande.html")

@app.errorhandler(404)
def request_page_not_found(error):
    return render_template ("erro404.html")
