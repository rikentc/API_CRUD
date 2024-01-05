import os
import psycopg2

# app/__init__.py
from flask import Flask,request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Criando instâncias
app = Flask(__name__)

api = Api(app)


# Configurando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@127.0.0.1:5432/Universidade'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Configurando Swagger com flasgger
swagger = Swagger(app)

# Exemplo de recurso
class HelloWorld(Resource):
    """
    Esta é uma descrição mais longa da sua API.
    Você pode incluir informações detalhadas sobre como usar esta rota.

    ---
    tags:
      - Hello
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: O nome para cumprimentar
    responses:
      200:
        description: Uma mensagem de saudação
    """
    def get_db_connection():
      conn = psycopg2.connect(host='localhost',
                            database='Universidade',
                            user='postgres',
                            password='admin')
      return conn

    def get(self):
        """
        Consultar todos os alunos.

        Retorna uma lista de alunos.

        ---
        produces:
          - application/json
        responses:
          200:
            description: Lista de alunos
        """

        conn = psycopg2.connect(host='localhost',
                            database='Universidade',
                            user='postgres',
                            password='admin')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Alunos;')
        books = cur.fetchall()
        cur.close()
        conn.close()
        return books

    def post(self):
        """
        Adicionar um novo aluno.

        Adiciona um novo aluno ao banco de dados com base nas informações fornecidas.

        ---
        consumes:
          - application/json
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  description: O nome do aluno
                cpf:
                  type: string
                  description: O CPF do aluno (11 dígitos)
                observacao:
                  type: string
                  description: Observação sobre o aluno
                idade:
                  type: integer
                  description: A idade do aluno
        responses:
          201:
            description: Aluno adicionado com sucesso
        """
        conn = psycopg2.connect(host='localhost',
                            database='Universidade',
                            user='postgres',
                            password='admin')
        cur = conn.cursor()

        dados_aluno = request.get_json()

        ins = cur.execute('INSERT INTO Alunos (nome, cpf, observacao, idade) VALUES (%s, %s, %s, %s)',
                          (dados_aluno['nome'], dados_aluno['cpf'], dados_aluno['observacao'], dados_aluno['idade']))
        
                
        conn.commit()
        cur.close()
        conn.close()

        return {'message': 'Aluno adicionado com sucesso'}, 201
       

# Adicionando recursos à instância 'api'
api.add_resource(HelloWorld, '/Alunos')

# Restante do seu código...

if __name__ == '__main__':
    app.run(debug=True)
