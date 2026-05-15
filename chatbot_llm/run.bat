@echo off
REM Script de inicialização para Windows

echo.
echo Iniciando Chatbot de Arquitetura de Computadores...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado. Instale Python 3.8 ou superior.
    pause
    exit /b 1
)

echo Python encontrado: 
python --version
echo.

REM Verificar se arquivo .env existe
if not exist ".env" (
    echo Arquivo .env não encontrado!
    echo Criando .env a partir de .env.example...
    
    if exist ".env.example" (
        copy .env.example .env
        echo Arquivo .env criado!
        echo.
        echo IMPORTANTE: Edite o arquivo .env e adicione sua chave de API do Groq!
        echo    Abra .env e configure: GROQ_API_KEY=sua_chave_aqui
        echo.
        set /p openfile="Abrir .env agora? (s/n): "
        if /i "%openfile%"=="s" (
            notepad .env
        )
    )
)

REM Verificar se venv existe
if not exist "venv" (
    echo.
    echo Ambiente virtual não encontrado. Criando...
    python -m venv venv
    echo Ambiente virtual criado!
)

echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependências...
pip install -r requirements.txt --quiet

echo.
echo Tudo pronto!
echo.
echo Iniciando servidor Flask...
echo    Acesse: http://localhost:5000
echo.
echo Dica: Abra http://localhost:5000 no seu navegador para usar o chatbot
echo.

python backend.py

pause
