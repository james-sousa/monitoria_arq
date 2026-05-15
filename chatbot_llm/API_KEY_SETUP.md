# Como Obter a Chave de API do Groq

## Passo 1: Acessar Groq
1. Abra seu navegador
2. Acesse: https://console.groq.com
3. Clique em "Sign Up" (Inscrever-se) ou "Sign In" (Entrar)

## Passo 2: Criar uma Conta (se necessário)
1. Clique em "Sign Up"
2. Escolha a opção de inscrição (Email, Google, GitHub, etc.)
3. Complete o cadastro
4. Verifique seu email se necessário

## Passo 3: Obter a Chave de API

### Passo a Passo:
1. Após fazer login, acesse: https://console.groq.com/keys
2. Clique em "Create API Key"
3. Escolha um nome para a chave (ex: "Chatbot Arquitetura")
4. Copie a chave exibida (começa com `gsk_`)

## Passo 4: Configurar no Projeto

1. Abra o arquivo `.env` na pasta do projeto (ou crie um a partir de `.env.example`)
2. Adicione sua chave:
   ```
   GROQ_API_KEY=gsk_XXXXXXXXXXXXXX
   ```
3. **Importante:** Nunca compartilhe esta chave!

## Plano Gratuito do Groq

- **Modelos Gratuitos:** Llama 2 70B é completamente gratuito para teste
- **Limite de Requisições:** Verifique no dashboard seu limite atual
- **Custo:** Sem custos diretos (por enquanto)
- **Saldo:** Você pode monitorar seu uso no console

## Verificar Sua Chave

Após configurar, ao iniciar o chatbot:
1. Abra `http://localhost:5000`
2. Verifique se o indicador de status mostra "Online"
3. Faça uma pergunta de teste

Se mostrar erro de autenticação:
- Verifique se copiou a chave inteira corretamente
- Certifique-se de que o arquivo `.env` está na pasta raiz do projeto
- Reinicie o servidor Python

## Segurança

- **Nunca commit o arquivo `.env` no Git!**
- **Nunca compartilhe sua chave de API**
- Se sua chave for exposta, delete-a em https://console.groq.com/keys e crie uma nova
- O arquivo `.gitignore` já deve estar configurado para ignorar `.env`

## Gerenciamento de Créditos

1. Acesse seu console em https://console.groq.com
2. Veja seu uso e limite de requisições
3. Monitore a velocidade de resposta
4. O Groq é conhecido por ser ultra-rápido!

## Suporte Groq

Se tiver problemas:
- Visite: https://console.groq.com/docs
- Veja a documentação da API
- Entre em contato com o suporte do Groq

---

**Dica:** O Groq é ultra-rápido! Prepare-se para respostas instantâneas! 
