
#Talysma,Ana Sales,Ravena,Maria Luiza#


from flask import Flask, redirect, url_for, session,request,render_template,jsonify
from flask.scaffold import F
from flask_restful import Api
from classes.contato import Contato
from model import db
import os
import secrets
from passlib.hash import sha256_crypt


from classes.cadastro import Cadastro
from classes.autenticacao import Autenticacao
from classes.perfil import Perfil
from classes.sair import Sair
from classes.foto import Foto
from classes.postagem import Postagem
from classes.postagens import Postagens
from classes.contato import Contato
from classes.contatos import Contatos
from classes.feed import Feed
from classes.curtida import Curtida
from classes.curtidas import Curtidas




app = Flask(__name__)
api = Api(app)

api.add_resource(Cadastro, '/api/cadastro')
api.add_resource(Autenticacao, '/api/autenticacao/<login>/<senha>')
api.add_resource(Perfil, '/api/perfil/<login>')
api.add_resource(Sair, '/api/sair')
api.add_resource(Foto, '/api/foto/<login>')
api.add_resource(Postagem,'/api/postagem')
api.add_resource(Postagens,'/api/postagens/<login>')
api.add_resource(Contato  ,'/api/contato/<login>')
api.add_resource(Contatos  ,'/api/contatos')
api.add_resource(Feed  ,'/api/feed')
api.add_resource(Curtida ,'/api/curtida/<id_postagem>')
api.add_resource(Curtidas ,'/api/curtidas/<id_postagem>')


app.secret_key = b'kljHI@gilds][s-39SIHD;.,&s'

app.config['PERFIL_FOLDER'] = 'static/img/perfil'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1000
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()  in ALLOWED_EXTENSIONS
 

@app.route("/")
def index():
    if "usuario" in session:
        lista=Feed.pega_postagens(session['id_user']) 

        for i in range (len(lista)):
            resultado = db.esta_curtindo(session['id_user'],lista[i]["id_post"])
            if resultado == None:
                lista[i]["curtiu"] = False
            else:
                lista[i]["curtiu"] = True

            
  
        
        return render_template("index.html", login = session['usuario'],eu=session['usuario'],postagens=lista)
    
       
        
    else:
        return render_template("login.html")



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
                session["id_user"] = usuario["id_user"]
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
        postagens=db.lista_mensagens(usuario['id_user'])
        

        resultado=db.esta_seguindo(session['id_user'],usuario['id_user'])
        if resultado==None:
            seguindo=False

        else:
            seguindo=True

        lista=[]
        for postagem in postagens:
            item={
                "id_post":postagem["id_post"],
                "datahora":postagem["datahora"],
                "texto":postagem["texto"]
                }

            resultado = db.esta_curtindo(session['id_user'],postagem["id_post"])
            if resultado == None:
                item["curtiu"] = False
            else:
                item["curtiu"] = True
            lista.append(item)







        return render_template("perfil.html", usuario=usuario, eu=session["usuario"],postagens=lista,login=session["usuario"],seguindo=seguindo)



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

@app.route("/postar", methods=["GET", "POST"])
def postar_web():
    if request.method == "GET":
        return render_template ('postar.html',login=session["usuario"])
    else:
        try:
            texto = request.form['texto']
            if texto == '':
                return  'Não pode texto em branco.'
            db.posta_mensagem(session['id_user'],texto)
            return index()
                              
        except KeyError:
            return 'Falta informar o texto.'


@app.route("/seguir/<login>")
def web_seguir(login):
    perfil = db.busca_usuario(login)
    if perfil==None:
        return  f'Usuário {login} não existe.'

    db.seguir(session['id_user'] ,perfil['id_user'])
    return redirect(url_for("perfil_web",login=login))

@app.route("/desseguir/<login>")
def web_desseguir(login):
    perfil = db.busca_usuario(login)
    if perfil==None:
        return  f'Usuário {login} não existe.'

    db.desseguir(session['id_user'] ,perfil['id_user'])
    return redirect(url_for("perfil_web",login=login))



@app.route("/curtir/<id_postagem>")
def web_curtir(id_postagem):
    postagem=db.pega_postagem(id_postagem)
    if postagem==None:
        return 'Postagem não existe.'

    resultado = db.curtir(session['id_user'] ,id_postagem)
    return redirect(url_for("index"))


@app.route("/descurtir/<id_postagem>")
def web_descurtir(id_postagem):
    postagem=db.pega_postagem(id_postagem)
    if postagem==None:
        return 'Postagem não existe.'

    resultado = db.descurtir(session['id_user'] ,id_postagem)
    return redirect(url_for("index"))



@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template ("arquivogrande.html")

@app.errorhandler(404)
def request_page_not_found(error):
    return render_template ("erro404.html")
