from flask import Flask, request, render_template, jsonify
import requests
import base64
import json
from datetime import datetime

app = Flask(__name__)

# Configurações da API
host = '45.189.16.4'
url = "https://ixc.mundonetbandalarga.com.br/webservice/v1/contato"
token = "15:aa71f1cb39a98ed7d20f55f7a9bf91c5fc750b5636847ddfca441a3d0b7dea73".encode('utf-8')

# Página inicial com o formulário
@app.route('/')
def index():
    # Passa a data atual para o formulário
    data_atual = datetime.now().strftime('%Y-%m-%d')
    return render_template('formulario.html', data_atual=data_atual)

# Rota para receber os dados do formulário
@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        # Coletar dados do formulário
        nome = request.form.get('nome', '')
        endereco = request.form.get('endereco', '')
        cep = request.form.get('cep', '')
        numero = request.form.get('numero', '')
        bairro = request.form.get('bairro', '')
        complemento = request.form.get('complemento', '')
        fone_celular = request.form.get('fone_celular', '')
        cnpj_cpf = request.form.get('cnpj_cpf', '')  # Correção para cnpj_cpf
        data_nascimento = request.form.get('data_nascimento', '')
        
        # Formatar a data de nascimento no formato 'dd/mm/aaaa'
        if data_nascimento:
            data_nascimento_formatada = datetime.strptime(data_nascimento, '%Y-%m-%d').strftime('%d/%m/%Y')
        else:
            data_nascimento_formatada = ''

        # Data de cadastro preenchida automaticamente com a data atual
        data_cadastro = datetime.now().strftime('%Y-%m-%d')

        # Verificação de dados obrigatórios
        if not nome or not endereco or not cep or not numero or not bairro or not fone_celular or not cnpj_cpf or not data_nascimento_formatada:
            return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios!'})

        # Montar o payload
        data = {
            'nome': nome,
            'endereco': endereco,
            'cep': cep,
            'numero': numero,
            'bairro': bairro,
            'complemento': complemento,
            'fone_celular': fone_celular,
            'cnpj_cpf': cnpj_cpf,  # Usando cnpj_cpf agora
            'referencia': data_nascimento_formatada,  # Enviar data formatada para o campo referência
            'data_cadastro': data_cadastro
        }

        # Configurar headers e payload
        headers = {
            'ixcsoft': '',
            'Authorization': 'Basic {}'.format(base64.b64encode(token).decode('utf-8')),
            'Content-Type': 'application/json'
        }

        # Fazer a requisição POST
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # Verificar o status da resposta da API
        if response.status_code == 200:
            return jsonify({'success': True, 'message': 'Dados enviados com sucesso!'})
        else:
            return jsonify({'success': False, 'message': 'Erro ao enviar dados!', 'details': response.text})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno no servidor', 'details': str(e)})

# Executar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
