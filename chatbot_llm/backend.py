from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração Groq
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Sistema de prompt para especialização em arquitetura de computadores
SYSTEM_PROMPT = """Você é um assistente especializado em Arquitetura e Organização de Computadores. 
Sua função é responder perguntas dos alunos sobre:
- Arquitetura de processadores
- Hierarquia de memória (cache, RAM, disco)
- Sistemas de numeração e representação de dados
- Organização de CPU (barramento, registradores, ciclo de instruções)
- Pipelining e paralelismo
- Componentes de hardware (ALU, unidade de controle, etc)
- Protocolos de comunicação
- Organização de entrada/saída

Sempre forneça respostas claras, educacionais e bem estruturadas. 
Se a pergunta não for relacionada a arquitetura de computadores, gentilmente redirecione o usuário."""

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para processar mensagens de chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Mensagem vazia'}), 400
        
        if not GROQ_API_KEY:
            return jsonify({'error': 'API key não configurada. Configure GROQ_API_KEY'}), 500
        
        # Preparar payload para Groq
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",  # Modelo Llama 3.3 do Groq
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        # Fazer requisição ao Groq
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"Erro Groq: {response.status_code} - {response.text}")
            return jsonify({'error': f'Erro na API: {response.status_code}'}), response.status_code
        
        result = response.json()
        
        # Extrair resposta
        if 'choices' in result and len(result['choices']) > 0:
            assistant_message = result['choices'][0]['message']['content']
            return jsonify({
                'success': True,
                'response': assistant_message
            })
        else:
            return jsonify({'error': 'Resposta inválida da API'}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Timeout na requisição (30s)'}), 408
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição: {e}")
        return jsonify({'error': f'Erro na requisição: {str(e)}'}), 500
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/')
def index():
    """Servir página inicial"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Verificar status da API"""
    return jsonify({
        'status': 'ok',
        'api_configured': bool(GROQ_API_KEY)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
