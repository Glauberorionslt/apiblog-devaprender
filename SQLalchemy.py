from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, true


# Criar a API FLASK
app = Flask(__name__)
#Criar instancia do SQL ALCHEMY
app.config['SECRET KEY'] = 'GLAUBER@2907'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

# tabela postagem
class Postagem(db.Model):
    #nome da tabela
    __tablename__ = 'postagem'
    #nome dos campos
    id_postagem =  db.Column(db.Integer,primary_key = True)
    titulo      =  db.Column(db.String)
    id_autor    =  db.Column(db.Integer,db.ForeignKey('autor.id_autor'))

 #Tabela Autor

class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer,primary_key = True)
    nome  =    db.Column(db.String)
    email =    db.Column(db.String)
    senha =    db.Column(db.String)
    admin =    db.Column(db.String)
    postagens = db.relationship('Postagem')

#executar o comando para criar banco de dados.
def inicializar_banco():
 db.drop_all()
 db.create_all()
 autor = Autor(nome ='glauber', email ='glauber@email.com',senha = '2907', admin = True)
 db.session.add(autor)
 db.session.commit()

if __name__ =="__main__":
    inicializar_banco()




