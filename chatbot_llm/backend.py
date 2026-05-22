from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import os
import json
from dotenv import load_dotenv
from tool_gerar_pdf import tool_gerar_pdf
load_dotenv()

app = Flask(__name__)
CORS(app)

# ─── Configuração OpenRouter ────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "~anthropic/claude-haiku-latest"   # troque por qualquer modelo do OpenRouter

# ─── Memória de conversas (em memória RAM; use Redis/DB para produção) ──────
# Estrutura: { session_id: [{"role": ..., "content": ...}, ...] }
conversations: dict[str, list] = {}

# ─── System prompt do agente ─────────────────────────────────────────────────
SYSTEM_PROMPT = """Você é um agente especializado em Arquitetura e Organização de Computadores.
Você pode raciocinar em múltiplos passos antes de responder. Quando necessário, use as ferramentas
disponíveis chamando-as no formato JSON descrito abaixo.

Ferramentas disponíveis:
- calcular_binario: converte números entre bases (decimal, binário, hexadecimal, octal)
  Parâmetros: {"numero": int, "de_base": int, "para_base": int}
- calcular_cache: simula hits/misses em cache dado tamanho e sequência de acessos
  Parâmetros: {"tamanho_cache": int, "acessos": [int]}
- explicar_instrucao: retorna detalhes de uma instrução de máquina MIPS/x86
  Parâmetros: {"instrucao": str}
- gerar_pdf: gera um PDF educacional (resumo, exercícios ou ficha de referência)
  Parâmetros: {
    "tipo": "resumo" | "exercicios" | "ficha",
    "titulo": str,
    "topico": str,
    "secoes": [{"titulo": str, "conteudo": str}],
    "questoes": [{"enunciado": str, "gabarito": str}],
    "tabela": {"cabecalho": [str], "linhas": [[str]]}
  }

- buscar_web: pesquisa na web via DuckDuckGo e retorna os principais resultados
  Parâmetros: {"query": str, "max_resultados": int}


Para usar uma ferramenta, responda EXATAMENTE assim (nenhum texto antes):
<tool_call>
{"tool": "nome_da_tool", "params": {...}}
</tool_call>

Após receber o resultado da ferramenta, use-o para formular a resposta final.
Se não precisar de ferramenta, responda diretamente de forma educacional e clara.

Tópicos que você domina: arquitetura de processadores, hierarquia de memória,
sistemas de numeração, organização de CPU, pipelining, paralelismo, ALU,
unidade de controle, protocolos de I/O.

Se a pergunta não for da área, redirecione gentilmente.

REGRA OBRIGATÓRIA PARA PDF:

calcular_binario:
- Use sempre que o usuário pedir conversão entre bases numéricas.
- Apresente o resultado de forma didática, explicando o processo de conversão.

calcular_cache:
- Use quando o usuário fornecer uma sequência de acessos e quiser simular o comportamento do cache.
- Explique o resultado destacando a taxa de hit e o impacto no desempenho.

explicar_instrucao:
- Use quando o usuário perguntar sobre uma instrução específica MIPS ou x86.
- Complemente o resultado da ferramenta com contexto adicional quando relevante.

buscar_web:
- Use sempre que o usuário perguntar sobre eventos recentes, lançamentos, notícias,
  benchmarks, papers ou qualquer informação que possa estar desatualizada no seu treinamento.
- Use também quando o usuário pedir explicitamente para "pesquisar", "buscar" ou "procurar".
- Após receber os resultados, você DEVE OBRIGATORIAMENTE:
  1. Basear sua resposta APENAS nas informações retornadas pela ferramenta, não no seu treinamento.
  2. Citar todas as fontes ao final no formato: Fontes: [título](url).
  3. Se a ferramenta retornar erro ou nenhum resultado, informe o usuário e responda
    com base no seu conhecimento, deixando claro que são dados do treinamento.

Só chame a ferramenta gerar_pdf se o usuário EXPLICITAMENTE pedir um PDF,
usar palavras como "gere", "crie", "faça", "baixar", "exportar" junto com "PDF",
"arquivo" ou "documento". Respostas normais de explicação NUNCA devem gerar PDF.
Ao montar os parâmetros da ferramenta gerar_pdf, cada seção deve ter conteúdo
DETALHADO e COMPLETO — mínimo de 3 parágrafos por seção, explicando o conceito
em profundidade, com exemplos práticos, fórmulas quando aplicável e contexto.
Nunca envie seções com apenas 1 ou 2 frases. O PDF deve ser rico o suficiente
para servir como material de estudo completo para um aluno de graduação.

Quando a ferramenta gerar_pdf retornar sucesso, sua resposta final DEVE
obrigatoriamente conter a linha abaixo, copiando exatamente o caminho retornado:
Arquivo: /tmp/pdfs_agente/nome_do_arquivo.pdf
Não explique como servir o arquivo, não mostre código Flask.
Apenas confirme a geração em uma frase e inclua a linha Arquivo: com o caminho completo."""

# ─── Implementação das ferramentas ──────────────────────────────────────────

def tool_calcular_binario(numero: int, de_base: int, para_base: int) -> str:
    try:
        valor = int(str(numero), de_base)
        if para_base == 2:
            resultado = bin(valor)[2:]
            nome = "binário"
        elif para_base == 16:
            resultado = hex(valor)[2:].upper()
            nome = "hexadecimal"
        elif para_base == 8:
            resultado = oct(valor)[2:]
            nome = "octal"
        else:
            resultado = str(valor)
            nome = "decimal"
        return f"{numero} (base {de_base}) = {resultado} ({nome}, base {para_base})"
    except Exception as e:
        return f"Erro na conversão: {e}"


def tool_calcular_cache(tamanho_cache: int, acessos: list[int]) -> str:
    cache = []
    hits = 0
    misses = 0
    log = []
    for addr in acessos:
        if addr in cache:
            hits += 1
            log.append(f"  Endereço {addr}: HIT  | cache={cache}")
        else:
            misses += 1
            if len(cache) >= tamanho_cache:
                removido = cache.pop(0)
                log.append(f"  Endereço {addr}: MISS | evicção de {removido} | cache={cache + [addr]}")
            else:
                log.append(f"  Endereço {addr}: MISS | cache={cache + [addr]}")
            cache.append(addr)
    taxa = (hits / len(acessos) * 100) if acessos else 0
    resumo = "\n".join(log)
    return (f"Simulação de cache (tamanho={tamanho_cache}, política=FIFO):\n{resumo}\n"
            f"Resultado: {hits} hits, {misses} misses, taxa de hit = {taxa:.1f}%")


def tool_explicar_instrucao(instrucao: str) -> str:
    db = {
        "ADD":  "ADD rd, rs, rt — Soma rs e rt, armazena em rd. Tipo R. Usa ALU.",
        "LW":   "LW rt, offset(rs) — Carrega word da memória [rs+offset] em rt. Tipo I.",
        "SW":   "SW rt, offset(rs) — Grava rt na memória [rs+offset]. Tipo I.",
        "BEQ":  "BEQ rs, rt, label — Salta para label se rs == rt. Tipo I. Branch condicional.",
        "JMP":  "JMP target — Salto incondicional para endereço target. Tipo J.",
        "MOV":  "MOV dst, src — Copia valor de src para dst (x86). Vários modos de endereçamento.",
        "PUSH": "PUSH src — Decrementa ESP e grava src na pilha (x86).",
        "POP":  "POP dst — Lê topo da pilha em dst e incrementa ESP (x86).",
        "SUB":  "SUB rd, rs, rt — Subtrai rt de rs, armazena em rd. Tipo R.",
        "AND":  "AND rd, rs, rt — AND bit a bit de rs e rt. Tipo R.",
        "OR":   "OR rd, rs, rt — OR bit a bit de rs e rt. Tipo R.",
        "SLL":  "SLL rd, rt, shamt — Shift lógico à esquerda de rt por shamt bits. Tipo R.",
        "SRL":  "SRL rd, rt, shamt — Shift lógico à direita de rt por shamt bits. Tipo R.",
    }
    instrucao_upper = instrucao.strip().upper()
    return db.get(instrucao_upper,
                  f"Instrução '{instrucao}' não encontrada no banco local. "
                  f"Consulte o manual ISA correspondente.")

def tool_buscar_web(query: str, max_resultados: int = 4) -> str:
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(query, max_results=max_resultados))

        print(f"[DEBUG buscar_web] query='{query}' | resultados={len(resultados)}")
        for r in resultados:
            print(f"  - {r.get('title')} | {r.get('href')}")

        if not resultados:
            return "Nenhum resultado encontrado para a busca."

        linhas = []
        for i, r in enumerate(resultados, 1):
            titulo = r.get("title", "Sem título")
            corpo  = r.get("body", "")
            url    = r.get("href", "")
            linhas.append(f"{i}. {titulo}\n   {corpo}\n   Fonte: {url}")

        return "\n\n".join(linhas)

    except Exception as e:
        return f"ERRO: {type(e).__name__}: {e}"



TOOLS = {
    "calcular_binario": tool_calcular_binario,
    "calcular_cache": tool_calcular_cache,
    "explicar_instrucao": tool_explicar_instrucao,
    "gerar_pdf":          tool_gerar_pdf,
    "buscar_web":   tool_buscar_web,
}

# ─── Loop do agente (ReAct: Reason → Act → Observe → Reason…) ───────────────

def chamar_llm(messages: list) -> str:
    """Faz uma chamada ao OpenRouter e retorna o texto da resposta."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "AgenteArquitetura",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4000,
    }
    resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def executar_tool(tool_call_text: str) -> str:
    """Extrai e executa o JSON de tool_call, retornando o resultado como string."""
    try:
        inicio = tool_call_text.find("{")
        fim = tool_call_text.rfind("}") + 1
        obj = json.loads(tool_call_text[inicio:fim])
        nome = obj["tool"]
        params = obj.get("params", {})
        if nome not in TOOLS:
            return f"Ferramenta '{nome}' não existe."
        return TOOLS[nome](**params)
    except Exception as e:
        return f"Erro ao executar ferramenta: {e}"


def rodar_agente(session_id: str, user_message: str, max_iteracoes: int = 5) -> dict:
    """
    Loop ReAct:
    1. Adiciona mensagem do usuário ao histórico
    2. Chama o LLM
    3. Se a resposta contém <tool_call>, executa a tool e adiciona o resultado
    4. Repete até resposta final ou limite de iterações
    """
    if session_id not in conversations:
        conversations[session_id] = []

    historico = conversations[session_id]
    historico.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + historico
    tool_calls_feitos = []

    for iteracao in range(max_iteracoes):
        resposta = chamar_llm(messages)

        if "<tool_call>" in resposta:
            # Extrai o bloco da tool
            ini = resposta.find("<tool_call>") + len("<tool_call>")
            fim = resposta.find("</tool_call>")
            tool_call_json = resposta[ini:fim].strip()

            resultado = executar_tool(tool_call_json)
            tool_calls_feitos.append({
                "chamada": tool_call_json,
                "resultado": resultado,
            })

            # Adiciona ao histórico: assistente pensou → tool → resultado
            messages.append({"role": "assistant", "content": resposta})
            messages.append({
                "role": "user",
                "content": f"[Resultado da ferramenta]: {resultado}"
            })
        else:
            # Resposta final
            historico.append({"role": "assistant", "content": resposta})
            conversations[session_id] = historico[-40:]  # mantém últimas 20 trocas
            return {
                "success": True,
                "response": resposta,
                "tool_calls": tool_calls_feitos,
                "iteracoes": iteracao + 1,
            }

    # Caso o limite seja atingido, retorna o que o LLM tiver dito por último
    historico.append({"role": "assistant", "content": resposta})
    return {
        "success": True,
        "response": resposta,
        "tool_calls": tool_calls_feitos,
        "iteracoes": max_iteracoes,
        "aviso": "Limite de iterações atingido.",
    }

# ─── Endpoints Flask ─────────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Mensagem vazia"}), 400
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "OPENROUTER_API_KEY não configurada"}), 500

        resultado = rodar_agente(session_id, user_message)
        return jsonify(resultado)

    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout (60s)"}), 408
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Erro OpenRouter: {e.response.status_code}"}), 502
    except Exception as e:
        app.logger.exception("Erro no agente")
        return jsonify({"error": str(e)}), 500


@app.route("/api/history/<session_id>", methods=["GET"])
def get_history(session_id):
    """Retorna o histórico de uma sessão."""
    return jsonify(conversations.get(session_id, []))


@app.route("/api/history/<session_id>", methods=["DELETE"])
def clear_history(session_id):
    """Limpa a memória de uma sessão."""
    conversations.pop(session_id, None)
    return jsonify({"cleared": True})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": MODEL,
        "api_configured": bool(OPENROUTER_API_KEY),
        "sessions_ativas": len(conversations),
    })

@app.route("/api/pdf/<nome>")
def servir_pdf(nome):
    caminho = f"/tmp/pdfs_agente/{nome}"
    return send_file(caminho, as_attachment=True, download_name=nome)

@app.route("/api/pdfs")
def listar_pdfs():
    arquivos = glob.glob("/tmp/pdfs_agente/*.pdf")
    return jsonify([os.path.basename(f) for f in sorted(arquivos)])

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")