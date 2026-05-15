# Chatbot - Arquitetura e Organização de Computadores

Um chatbot simples em **Python puro** (sem dependências externas) para tirar dúvidas sobre a disciplina de Arquitetura e Organização de Computadores.

## Características

- ✅ **Python Puro**: Sem dependências externas
- ✅ **Base de Conhecimento**: Abrange tópicos principais da disciplina
- ✅ **Busca por Palavras-chave**: Encontra respostas relevantes
- ✅ **Interface Simples**: Chat interativo no terminal
- ✅ **Histórico de Perguntas**: Mantém registro de conversas

## Como Usar

### Executar o chatbot:

```bash
python3 chatbot.py
```

### Comandos disponíveis:

- **Pergunta natural**: Digite qualquer pergunta sobre o assunto
  - Exemplos: "O que é CPU?", "Como funciona cache?", "Explique pipeline"
  
- **`tópicos`**: Lista todos os tópicos disponíveis

- **`ajuda`**: Mostra comandos e tópicos principais

- **`sair` ou `quit`**: Finaliza a conversa

## Tópicos Disponíveis

### CPU e Processamento
- `cpu` - Unidade Central de Processamento
- `processador` - Sinônimo de CPU
- `registrador` - Memórias rápidas dentro da CPU
- `alu` - Unidade Lógica e Aritmética

### Memória
- `memória` - Hierarquia de memória
- `ram` - Memória de Acesso Aleatório
- `cache` - Memória intermediária
- `disco` - Armazenamento permanente

### Execução
- `ciclo` - Ciclo de busca-execução
- `instrução` - Operações da CPU
- `clock` - Sinal de sincronização
- `barramento` - Caminho de comunicação

### Arquitetura
- `arquitetura` - Estudo da organização
- `von neumann` - Arquitetura clássica
- `harvard` - Arquitetura alternativa

### Conceitos Avançados
- `pipeline` - Paralelismo de instruções
- `bit` - Unidade menor de informação
- `byte` - 8 bits
- `endereçamento` - Modos de acesso
- `interrupção` - Desvios de execução

## Exemplos de Uso

```
Você: O que é CPU?
Chatbot: A CPU (Unidade Central de Processamento) é o "cérebro" do computador...

Você: Explique memória cache
Chatbot: Cache é memória muito rápida entre CPU e RAM...

Você: Como funciona pipeline?
Chatbot: Pipeline permite paralelismo ao dividir a execução em estágios...

Você: tópicos
Chatbot: (lista todos os tópicos disponíveis)

Você: sair
Chatbot: Até logo! Continue estudando!
```

## Estrutura do Código

```
ChatbotArquitetura
├── __init__() - Inicializa com base de conhecimento
├── _criar_base_conhecimento() - Cria dicionário de respostas
├── _extrair_palavras_chave() - Processa entrada
├── _buscar_resposta() - Encontra melhor resposta
├── _resposta_padrao() - Resposta para não encontrado
├── responder() - Responde pergunta
├── listar_topicos() - Lista tópicos
└── processar_comando() - Processa entrada do usuário
```

## Como Estender

Para adicionar novos tópicos, edite a função `_criar_base_conhecimento()`:

```python
"novo_topico": """Descrição completa do tópico...""",
```

## Notas

- O chatbot usa busca simples por palavras-chave
- Responde com base na similaridade textual
- Mantém histórico de perguntas (pode ser usado para análise)
- Interface amigável e intuitiva

## Autor

Desenvolvido como assistente de monitoria para a disciplina de Arquitetura e Organização de Computadores.

---

**Bom estudo!** 
