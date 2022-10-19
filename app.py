from ast import Return
from enum import auto
import json
from lib2to3.pgen2 import token
from multiprocessing.util import abstract_sockets_supported
from textwrap import wrap
from flask import Flask, jsonify, request, make_response
from SQLalchemy import Autor, Postagem, db
import jwt
from datetime import datetime,timedelta

app = Flask(__name__)

# postagens = [
#     {
#         'título': 'Minha História',
#         'autor': 'Amanda Dias'
#     },
#     {
#         'título': 'Novo Dispositivo Sony',
#         'autor': 'Howard Stringer'
#     },
#     {
#         'título': 'Lançamento do Ano',
#         'autor': 'Jeff Bezos'
#     },
# ]
# # Rota padrão - GET https://localhost:5000


# @app.route('/')
# def obter_postagens():
#     return jsonify(postagens)

# # Obter postagem por id - GET https://localhost:5000/postagem/1


# @app.route('/postagem/<int:indice>', methods=['GET'])
# def obter_postagem_por_indice(indice):
#     return jsonify(postagens[indice])

# # Criar uma nova postagem - POST https://localhost:5000/postagem


# @app.route('/postagem', methods=['POST'])
# def nova_postagem():
#     postagem = request.get_json()
#     postagens.append(postagem)

#     return jsonify(postagem, 200)

# # Alterar uma postagem existente - PUT https://localhost:5000/postagem/1


# @app.route('/postagem/<int:indice>', methods=['PUT'])
# def alterar_postagem(indice):
#     postagem_alterada = request.get_json()
#     postagens[indice].update(postagem_alterada)

#     return jsonify(postagens[indice], 200)

# # Excluir uma postagem - DELETE - https://localhost:5000/postagem/1


# # def excluir_postagem(indice):
#     try:
#         if postagens[indice] is not None:
#             del postagens[indice]
#             return jsonify(f'Foi excluído a postagem {postagens[indice]}', 200)
#     except:
#         return jsonify('Não foi possível encontrar a postagem para exclusão', 404)

#CONSTRUINDO API COM ESTRUTURA DE BANCO DE DADOS 
#POSTMAN & DBBROWSER

# Rota para Token obrigatório http://localhost:5000/http://localhost:5000
def token_obrigatorio(f):
    @wrap(f)
    def decorated(*args,**kargs):
        token:None
        #verificar se um token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if not token:
                return jsonify({'mensagem':'Token não encontrado'},401)
        #caso verdadeiro consultar bd
        try:
            resultado = jwt.decode(token,app.config['SECRET KEY'])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except: 
            return jsonify({'mensagem':'Token é invalido'},401)
        return f(autor,*args,**kargs)

    return decorated



# Rota para login http://localhost:5000/login
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login Invalido',401,{'www-Authenticate':'Basic realm=Login Obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login invalido',401,{'www-Authenticate':'Basic realm=Login Obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor,'exp':datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['GLAUBER@2907']) 
        return jsonify({'token':token})
    return make_response('Login Invalido', 401,{'www-Authenticate': 'Basic realm=Login Obrigatório"'})






#Rota para consulta autores GET

@app.route('/autores')
#@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)

    return jsonify({'autores': lista_de_autores})

#Rota para consulta autores GET p/ Id

@app.route('/autores/<int:id_autor>', methods=['GET'])
#@token_obrigatorio
def obter_autor_por_id(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first
    if not autor:
        return jsonify(f'Autor não encontrado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email

    return jsonify({'autor': autor_atual})

#Rota para inser~]ap de novo autor

@app.route('/autores', methods=['POST'])
#@token_obrigatorio
def novo_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(
        nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])
    db.session.add(autor)
    db.commit()
    return jsonify({'mensagem': 'Usuario criado com sucesso'}, 200)


@app.route('/autores/<int:id_autor>', methods=['PUT'])
#@token_obrigatorio
def alterar_autor(autor,id_autor):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()

    if not autor:
        return jsonify({'Mensagem': 'Este usuario nao foi encontrado'})
    try:
        if usuario_a_alterar['nome']:
            autor.nome = usuario_a_alterar['nome']
    except:
        pass
    try:
        if usuario_a_alterar['email']:
            autor.email = usuario_a_alterar['email']
    except:
        pass
    try:
        if usuario_a_alterar['senha']:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass

    db.session.commit()
    return jsonify({'Mensagem:' 'Usuario alterado com sucesso!'})


@app.route('/autores/<int:id_autor>', methods=['DELETE'])
def excluir_autor(id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'Mensagem': 'Este autor não existe'})
    db.session.delete(autor_existente)
    db.commit()


# Construindo a estrutura para Postagens

@app.route('/postagens')  # Metodo GET p/ postagens
def obterpostagens():
    postagens = Postagem.query.all()
    lista_de_postagens = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['id_postagem'] = postagem.id_postagem
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor

    lista_de_postagens.append(postagem_atual)
    return jsonify({'postagens': lista_de_postagens})

# Metodo GET com id para obter postagens por id

@app.route('/postagens/<int:id_postagem>', methods=['GET'])
def obterpostagem_id(id_postagem):
    postagem1 = Postagem.query.filter_by(id_postagem=id_postagem).first
    if not postagem1:
        return jsonify(f'Postagem não encontrada')

    postagem_atual = {}
    postagem_atual['id_postagem'] = Postagem.id_postagem
    postagem_atual['titulo'] = Postagem.titulo
    postagem_atual['id_autor'] = Postagem.id_autor

    return jsonify(f'Voce buscou pela postagem {postagem_atual}')

#Metodo POST para criação de novas postagens


@app.route('/postagens', methods=['POST'])
def novapostagem():
    nova_postagem = request.get_json()
    postagem = Postagem(titulo=nova_postagem['titulo'])

    db.session.add(postagem)
    db.commit()

    return jsonify({'mensagem':'usuario cadastrado com sucesso'},200)




#Metodo para alterar uma postagem

@app.route('/postagens/<int:id_postagem>',methods=['PUT'])
def alterarpostagem(id_postagem):
    postagem_a_alter = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem).first()

    if not postagem:
        return jsonify({'Mensagem':'Esta postagem não existe'})
   
    postagem_a_alter['titulo']
    Postagem.titulo = postagem_a_alter

    db.session()
    return jsonify({'Mesangem':'Postagem alterada com sucesso!'})   

 #Metodo Delete para postagens
@app.route('/postagens/<int:id_postagem>',methods=['DELETE'])
def deletarpostagem(id_postagem):
    postagem_existente = Postagem.query.filter_by(id_postagem=id_postagem).first
    if not postagem_existente:
        jsonify({'mensagem':'postagem não encontrada'})
        db.session.delete(postagem_existente)
        return jsonify({'mensagem':'postagem excluida com sucesso!'})   


    #coments

if __name__ == '__main__':

 app.run(port=5000, host='localhost', debug=True)