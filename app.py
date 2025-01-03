import os
from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo ao formulário de pré-cadastro da Mundonet!"

@app.route('/enviar', methods=['POST'])
def enviar_formulario():
    # Recebe os dados do formulário
    dados = request.json

    # Define os dados a serem enviados para a API (ajuste conforme sua necessidade)
    payload = json.dumps({
        'principal': 'N',
        'id_cliente': '',
        'nome': dados.get('nome'),
        'tipo_pessoa': 'F',
        'cpf_cnpj': dados.get('cpf_cnpj'),
        'data_nascimento': dados.get('data_nascimento'),
        'data_cadastro': dados.get('data_cadastro'),
        'email': dados.get('email'),
        'telefone': dados.get('telefone'),
        'cep': dados.get('cep'),
        'endereco': dados.get('endereco'),
        'numero': dados.get('numero'),
        'bairro': dados.get('bairro'),
        'complemento': dados.get('complemento'),
        'cidade': dados.get('cidade'),
        'uf': dados.get('uf'),
        'referencia': dados.get('referencia')
    })

    # URL da API de destino
    url = "https://ixc.mundonetbandalarga.com.br/webservice/v1/contato"
    
    # Cabeçalhos da requisição
    headers = {
        'Authorization': 'Basic seu_token_aqui',  # Coloque seu token aqui
        'Content-Type': 'application/json'
    }

    # Envia os dados para a API
    response = requests.post(url, data=payload, headers=headers)

    # Verifica a resposta da API
    if response.status_code == 200:
        return jsonify({
            "message": "Cadastro efetuado com sucesso! Em breve nossa equipe entrará em contato com você, obrigado",
            "success": True
        }), 200
    else:
        return jsonify({
            "message": "Erro ao enviar os dados. Tente novamente mais tarde.",
            "success": False
        }), 500

if __name__ == '__main__':
    # Pega a variável PORT, que é configurada automaticamente pelo Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
