# Chatbot de Arquitetura de Computadores com LLM

Um chatbot inteligente especializado em responder perguntas sobre Arquitetura e Organização de Computadores, construído com Python/Flask e interface HTML/CSS, alimentado pela API Groq.

## Características

- Interface web moderna e responsiva
- Respostas baseadas em LLM (usando Groq - muito rápido!)
- Especialização em Arquitetura de Computadores
- Suporte a tópicos como:
  - Arquitetura de processadores
  - Hierarquia de memória (cache, RAM, disco)
  - Sistemas de numeração
  - Pipelining e paralelismo
  - Componentes de hardware
  - E muito mais!

## Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Uma chave de API do Groq (gratuita em https://console.groq.com)

##  Instalação

### 1. Clonar/Baixar o Projeto
```bash
cd chatbot_llm
```

### 2. Criar um Ambiente Virtual (Recomendado)
```bash
python -m venv venv
```

**Ativar o ambiente virtual:**
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar a Chave de API

1. Acesse [https://console.groq.com](https://console.groq.com) e crie uma conta gratuita
2. Obtenha sua chave de API
3. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edite o arquivo `.env` e adicione sua chave:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxx
   ```

## Como Executar

1. Certifique-se que o ambiente virtual está ativado
2. Execute o servidor Flask:
   ```bash
   python backend.py
   ```
3. O servidor iniciará em `http://localhost:5000`
4. Abra seu navegador e acesse `http://localhost:5000`
5. Comece a fazer perguntas sobre Arquitetura de Computadores!

## Exemplos de Perguntas

Você pode fazer perguntas como:
- "O que é cache L1, L2 e L3?"
- "Explique o ciclo de instruções de uma CPU"
- "Como funciona o pipelining em processadores?"
- "Qual é a diferença entre DRAM e SRAM?"
- "Descreva a hierarquia de memória"
- "O que é bus de dados e barramento de endereço?"
- "Explique o funcionamento de uma ALU"
- "Como funciona a unidade de controle?"

## Estrutura do Projeto

```
chatbot_llm/
├── backend.py              # Servidor Flask
├── requirements.txt        # Dependências Python
├── .env.example           # Template de variáveis de ambiente
├── .env                   # Variáveis de ambiente (configure com sua chave)
├── templates/
│   └── index.html         # Interface do chat (HTML)
└── static/
    ├── style.css          # Estilos (CSS)
    └── script.js          # Lógica do frontend (JavaScript)
```

## Tecnologias Utilizadas

- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **API:** Groq (para modelos de LLM - ultra rápido!)
- **Comunição:** REST API com JSON

## Modelos Disponíveis

O chatbot está configurado para usar `llama2-70b-4096` que é gratuito no Groq. 

Você pode mudá-lo editando a linha no `backend.py`:
```python
"model": "llama2-70b-4096"
```

Veja outras opções em: https://console.groq.com/docs/models

## Configurações

### Alterar a Porta
Edite a última linha do `backend.py`:
```python
app.run(debug=True, port=5000, host='127.0.0.1')
```

### Ajustar Temperatura (Criatividade das Respostas)
No `backend.py`, mude:
```python
"temperature": 0.7,  # 0.0 = determinístico, 1.0 = criativo
```

### Alterar Limite de Tokens
No `backend.py`, mude:
```python
"max_tokens": 1000,  # Comprimento máximo da resposta
```

## Troubleshooting

### "API key não configurada"
- Verifique se o arquivo `.env` existe e contém sua chave válida
- Reinicie o servidor

### "Erro de conexão"
- Certifique-se que o servidor Flask está rodando (`python backend.py`)
- Verifique se está acessando `http://localhost:5000`

### "Timeout na requisição"
- A API está demorando demais para responder
- Tente novamente em alguns segundos
- Verifique sua conexão com a internet

### Módulos não encontrados
- Certifique-se de instalar as dependências: `pip install -r requirements.txt`
- Verifique se o ambiente virtual está ativado

## Notas de Segurança

- **Nunca compartilhe seu arquivo `.env`** com sua chave de API
- O arquivo `.env` deve estar no `.gitignore`
- A chave é sensível - mantenha-a segura

## Para Fins Educacionais

Este chatbot foi criado para ajudar estudantes de Arquitetura e Organização de Computadores. Use-o como ferramenta de aprendizagem complementar!

## Licença

Este projeto é fornecido como está, para fins educacionais.

## Suporte

Se encontrar problemas:
1. Verifique se todas as dependências estão instaladas
2. Certifique-se que a chave de API é válida
3. Verifique os logs do terminal para mensagens de erro
4. Redefina o servidor (Ctrl+C e execute novamente)

---

**Aproveite seu assistente de Arquitetura de Computadores! **
