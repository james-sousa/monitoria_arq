# Chatbot com Groq - Instruções Finais

## Tudo Está Pronto!

Seu chatbot foi atualizado para usar a **API Groq** - que é ultra-rápida e gratuita!

## Próximos Passos

### 1. Obter Chave Groq (Rápido!)
```bash
# Abra seu navegador e vá para:
# https://console.groq.com

# 1. Crie uma conta gratuita
# 2. Vá para https://console.groq.com/keys
# 3. Clique em "Create API Key"
# 4. Copie a chave (começa com gsk_)
```

### 2. Configurar no Projeto
```bash
# Abra o arquivo .env no projeto
# Edite a linha:
GROQ_API_KEY=gsk_XXXXXXXXXXXXXX
# ^^ Cole sua chave aqui
```

### 3. Iniciar o Servidor
```bash
# Linux/Mac:
./run.sh

# Windows:
run.bat
```

### 4. Usar o Chatbot
```bash
# Abra seu navegador em:
http://localhost:5000
```

## Diferenciais do Groq

| Recurso | Groq | OpenRouter |
|---------|------|-----------|
| **Velocidade** | Ultra-rápido | Rápido |
| **Custo** | Gratuito | Gratuito |
| **Latência** | 10-20x menor | Normal |
| **Modelos** | Llama 2 | Vários |
| **Limite** | Generoso | Limitado |

## 📋 Checklist de Configuração

- [ ] Criou conta em https://console.groq.com
- [ ] Obteve a chave de API (gsk_...)
- [ ] Editou o arquivo `.env`
- [ ] Executou `./run.sh` ou `run.bat`
- [ ] Acessou http://localhost:5000
- [ ] Fez uma pergunta de teste

## Dicas

1. **Primeira vez é lenta?** É normal - carregando o modelo
2. **Depois fica rápido?** Sim! O Groq é muito rápido
3. **Quer testar?** Pergunta sobre cache, CPU, memória
4. **Algum erro?** Verifique se a chave está no `.env`

## Suporte

Se tiver problemas:
- Verifique se `.env` tem a chave correta
- Reinicie o servidor (`Ctrl+C` e execute novamente)
- Veja https://console.groq.com/docs se tiver dúvidas sobre a API

## Começar a Usar

Exemplos de perguntas:
- "O que é cache L1, L2 e L3?"
- "Explique pipelining"
- "Qual é a hierarquia de memória?"
- "Como funciona uma CPU?"

---

**Aproveite a velocidade do Groq!**

Você está pronto para começar!
