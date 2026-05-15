#!/bin/bash

# Script de inicialização rápida para o Chatbot de Arquitetura

echo "Iniciando Chatbot de Arquitetura de Computadores..."
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Instale Python 3.8 ou superior."
    exit 1
fi

echo "Python encontrado: $(python3 --version)"
echo ""

# Verificar se arquivo .env existe
if [ ! -f ".env" ]; then
    echo "Arquivo .env não encontrado!"
    echo "Criando .env a partir de .env.example..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Arquivo .env criado!"
        echo ""
        echo "IMPORTANTE: Edite o arquivo .env e adicione sua chave de API do Groq!"
        echo "   Abra .env e configure: GROQ_API_KEY=sua_chave_aqui"
        echo ""
        read -p "Abrir .env agora? (s/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            if command -v nano &> /dev/null; then
                nano .env
            elif command -v vim &> /dev/null; then
                vim .env
            else
                echo "Use um editor para abrir o arquivo .env"
            fi
        fi
    fi
fi

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    echo "Ambiente virtual criado!"
fi

echo ""
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo ""
echo "Instalando dependências..."
pip install -r requirements.txt --quiet

echo ""
echo "Tudo pronto!"
echo ""
echo "Iniciando servidor Flask..."
echo "   Acesse: http://localhost:5000"
echo ""
echo "Dica: Abra http://localhost:5000 no seu navegador para usar o chatbot"
echo ""
python3 backend.py
