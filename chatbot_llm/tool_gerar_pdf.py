"""
tool_gerar_pdf.py
-----------------
Tool do agente de Arquitetura de Computadores para geração de PDFs educacionais.

Tipos suportados:
  - "resumo"    → texto expositivo com seções e tabela opcional
  - "exercicios"→ lista de questões numeradas com gabarito separado
  - "ficha"     → ficha compacta de referência rápida (conceitos + fórmulas)

Integração com o backend (backend_agente.py):
  1. Importe este módulo no backend
  2. Registre a função no dicionário TOOLS:
       from tool_gerar_pdf import tool_gerar_pdf
       TOOLS["gerar_pdf"] = tool_gerar_pdf
  3. Adicione a descrição da tool no SYSTEM_PROMPT do agente:
       - gerar_pdf: gera um PDF educacional (resumo, exercícios ou ficha de estudo)
         Parâmetros: {
           "tipo": "resumo" | "exercicios" | "ficha",
           "titulo": str,
           "topico": str,
           "secoes": [{"titulo": str, "conteudo": str}],          # para resumo/ficha
           "questoes": [{"enunciado": str, "gabarito": str}],     # para exercícios
           "tabela": {"cabecalho": [str], "linhas": [[str]]}      # opcional, para resumo
         }

O PDF é salvo em /tmp/ e o caminho retornado pode ser servido via endpoint Flask.
"""

import os
import uuid
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ─── Paleta ──────────────────────────────────────────────────────────────────
COR_PRIMARIA   = colors.HexColor("#4F46E5")   # indigo
COR_SECUNDARIA = colors.HexColor("#7C3AED")   # violeta
COR_FUNDO_LEVE = colors.HexColor("#EEF2FF")   # indigo 50
COR_FUNDO_ALT  = colors.HexColor("#F5F3FF")   # violeta 50
COR_BORDA      = colors.HexColor("#C7D2FE")   # indigo 200
COR_TEXTO      = colors.HexColor("#1E1B4B")   # indigo 950
COR_CINZA      = colors.HexColor("#6B7280")
COR_GABARITO   = colors.HexColor("#D1FAE5")   # green 100
COR_GABARITO_T = colors.HexColor("#065F46")   # green 800

OUTPUT_DIR = "/tmp/pdfs_agente"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─── Estilos ─────────────────────────────────────────────────────────────────
def _estilos():
    base = getSampleStyleSheet()
    return {
        "titulo_doc": ParagraphStyle(
            "titulo_doc", parent=base["Title"],
            fontSize=22, textColor=COR_PRIMARIA,
            spaceAfter=4, alignment=TA_CENTER, leading=26,
        ),
        "subtitulo": ParagraphStyle(
            "subtitulo", parent=base["Normal"],
            fontSize=11, textColor=COR_CINZA,
            spaceAfter=2, alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"],
            fontSize=14, textColor=COR_PRIMARIA,
            spaceBefore=16, spaceAfter=4, leading=18,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"],
            fontSize=12, textColor=COR_SECUNDARIA,
            spaceBefore=10, spaceAfter=3, leading=16,
        ),
        "corpo": ParagraphStyle(
            "corpo", parent=base["Normal"],
            fontSize=11, leading=17, spaceAfter=6,
            textColor=COR_TEXTO, alignment=TA_JUSTIFY,
        ),
        "codigo": ParagraphStyle(
            "codigo", parent=base["Normal"],
            fontSize=10, fontName="Courier", leading=14,
            backColor=COR_FUNDO_LEVE, textColor=COR_TEXTO,
            leftIndent=10, rightIndent=10,
            spaceBefore=4, spaceAfter=6,
        ),
        "questao_num": ParagraphStyle(
            "questao_num", parent=base["Normal"],
            fontSize=12, fontName="Helvetica-Bold",
            textColor=COR_PRIMARIA, spaceBefore=12, spaceAfter=2,
        ),
        "questao_txt": ParagraphStyle(
            "questao_txt", parent=base["Normal"],
            fontSize=11, leading=16, spaceAfter=4, textColor=COR_TEXTO,
        ),
        "gabarito": ParagraphStyle(
            "gabarito", parent=base["Normal"],
            fontSize=10, leading=15, textColor=COR_GABARITO_T,
            leftIndent=12,
        ),
        "ficha_label": ParagraphStyle(
            "ficha_label", parent=base["Normal"],
            fontSize=10, fontName="Helvetica-Bold",
            textColor=COR_PRIMARIA, spaceAfter=1,
        ),
        "ficha_valor": ParagraphStyle(
            "ficha_valor", parent=base["Normal"],
            fontSize=10, leading=14, textColor=COR_TEXTO, spaceAfter=6,
        ),
        "rodape": ParagraphStyle(
            "rodape", parent=base["Normal"],
            fontSize=8, textColor=COR_CINZA, alignment=TA_CENTER,
        ),
    }


# ─── Cabeçalho comum ─────────────────────────────────────────────────────────
def _cabecalho(story, titulo: str, topico: str, tipo_label: str, st: dict):
    story.append(Paragraph(titulo, st["titulo_doc"]))
    story.append(Paragraph(f"{tipo_label} · {topico}", st["subtitulo"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COR_PRIMARIA))
    story.append(Spacer(1, 0.4 * cm))


def _rodape(story, st: dict):
    data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=COR_BORDA))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        f"Gerado pelo Agente de Arquitetura de Computadores · {data_str}",
        st["rodape"],
    ))


# ─── Tabela estilizada ────────────────────────────────────────────────────────
def _tabela(cabecalho: list[str], linhas: list[list[str]]) -> Table:
    if not cabecalho:
        return None
    data = [cabecalho] + linhas
    col_w = 15.5 * cm / len(cabecalho)
    t = Table(data, colWidths=[col_w] * len(cabecalho), repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  COR_PRIMARIA),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, COR_FUNDO_LEVE]),
        ("GRID",          (0, 0), (-1, -1), 0.4, COR_BORDA),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    return t


# ─── Geradores por tipo ───────────────────────────────────────────────────────

def _gerar_resumo(doc, titulo, topico, secoes, tabela, st):
    story = []
    _cabecalho(story, titulo, topico, "Resumo", st)

    for sec in secoes:
        story.append(Paragraph(sec["titulo"], st["h1"]))
        # Suporte a múltiplos parágrafos separados por \n\n
        for paragrafo in sec["conteudo"].split("\n\n"):
            paragrafo = paragrafo.strip()
            if paragrafo.startswith("```") and paragrafo.endswith("```"):
                texto_codigo = paragrafo.strip("`").strip()
                story.append(Paragraph(texto_codigo.replace("\n", "<br/>"), st["codigo"]))
            elif paragrafo:
                story.append(Paragraph(paragrafo, st["corpo"]))
        story.append(Spacer(1, 0.2 * cm))

    if tabela:
        t = _tabela(tabela.get("cabecalho", []), tabela.get("linhas", []))
        if t is not None:
            story.append(Spacer(1, 0.3 * cm))
            story.append(t)

    _rodape(story, st)
    doc.build(story)


def _gerar_exercicios(doc, titulo, topico, questoes, st):
    story = []
    _cabecalho(story, titulo, topico, "Lista de Exercícios", st)

    for i, q in enumerate(questoes, 1):
        story.append(Paragraph(f"Questão {i}", st["questao_num"]))
        story.append(Paragraph(q["enunciado"], st["questao_txt"]))
        story.append(Spacer(1, 0.5 * cm))  # espaço para resposta escrita

    # Gabarito em página separada
    story.append(PageBreak())
    story.append(Paragraph("Gabarito", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=COR_PRIMARIA))
    story.append(Spacer(1, 0.3 * cm))

    gab_data = [[f"Q{i}", q["gabarito"]] for i, q in enumerate(questoes, 1)]
    t = Table(gab_data, colWidths=[1.5 * cm, 14 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), COR_GABARITO),
        ("TEXTCOLOR",     (0, 0), (0, -1),  COR_GABARITO_T),
        ("FONTNAME",      (0, 0), (0, -1),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#A7F3D0")),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    story.append(t)

    _rodape(story, st)
    doc.build(story)


def _gerar_ficha(doc, titulo, topico, secoes, st):
    story = []
    _cabecalho(story, titulo, topico, "Ficha de Referência Rápida", st)

    # Layout em duas colunas via Table
    celulas = []
    celula_atual = []
    for sec in secoes:
        bloco = [Paragraph(sec["titulo"], st["h2"])]
        for paragrafo in sec["conteudo"].split("\n\n"):
            paragrafo = paragrafo.strip()
            if paragrafo:
                if paragrafo.startswith("```"):
                    texto_codigo = paragrafo.strip("`").strip()
                    bloco.append(Paragraph(texto_codigo.replace("\n", "<br/>"), st["codigo"]))
                else:
                    bloco.append(Paragraph(paragrafo, st["ficha_valor"]))
        bloco.append(Spacer(1, 0.1 * cm))
        celula_atual.append(bloco)

        if len(celula_atual) == 2:
            celulas.append(celula_atual)
            celula_atual = []

    # Célula restante se ímpar
    if celula_atual:
        celula_atual.append([Spacer(1, 1)])  # célula vazia
        celulas.append(celula_atual)

    if celulas:
        # Achata blocos em listas de flowables para cada célula da tabela
        rows = []
        for par in celulas:
            rows.append([par[0], par[1]])

        t = Table(rows, colWidths=[7.5 * cm, 7.5 * cm],
                  style=TableStyle([
                      ("VALIGN",       (0, 0), (-1, -1), "TOP"),
                      ("LEFTPADDING",  (0, 0), (-1, -1), 8),
                      ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                      ("TOPPADDING",   (0, 0), (-1, -1), 4),
                      ("LINEAFTER",    (0, 0), (0, -1),  0.5, COR_BORDA),
                  ]))
        story.append(t)

    _rodape(story, st)
    doc.build(story)


# ─── Ponto de entrada da tool ─────────────────────────────────────────────────

def tool_gerar_pdf(
    tipo: str,
    titulo: str,
    topico: str,
    secoes: list | None = None,
    questoes: list | None = None,
    tabela: dict | None = None,
) -> str:
    """
    Gera um PDF educacional e retorna o caminho do arquivo.

    Parâmetros:
      tipo    : "resumo" | "exercicios" | "ficha"
      titulo  : título do documento (ex: "Pipeline de CPU")
      topico  : área do assunto (ex: "Organização de Computadores")
      secoes  : [{"titulo": str, "conteudo": str}]  — para resumo e ficha
      questoes: [{"enunciado": str, "gabarito": str}] — para exercícios
      tabela  : {"cabecalho": [str], "linhas": [[str]]} — opcional, só para resumo
    """
    # Limpar parâmetros vazios enviados pelo LLM
    if not questoes:
        questoes = None
    if not secoes:
        secoes = None
    if tabela and (not tabela.get("cabecalho") or not tabela.get("linhas")):
        tabela = None

    tipos_validos = ("resumo", "exercicios", "ficha")
    if tipo not in tipos_validos:
        return f"Tipo inválido '{{tipo}}'. Use: {', '.join(tipos_validos)}."

    st = _estilos()
    nome_arquivo = f"{tipo}_{uuid.uuid4().hex[:8]}.pdf"
    caminho = os.path.join(OUTPUT_DIR, nome_arquivo)

    doc = SimpleDocTemplate(
        caminho,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm,  bottomMargin=2 * cm,
        title=titulo,
        author="Agente de Arquitetura de Computadores",
    )

    try:
        if tipo == "resumo":
            if not secoes:
                return "Para 'resumo', forneça ao menos uma seção em 'secoes'."
            _gerar_resumo(doc, titulo, topico, secoes, tabela, st)

        elif tipo == "exercicios":
            if not questoes:
                return "Para 'exercicios', forneça ao menos uma questão em 'questoes'."
            _gerar_exercicios(doc, titulo, topico, questoes, st)

        elif tipo == "ficha":
            if not secoes:
                return "Para 'ficha', forneça ao menos uma seção em 'secoes'."
            _gerar_ficha(doc, titulo, topico, secoes, st)

        return (
            f"PDF gerado com sucesso!\n"
            f"Tipo: {tipo}\n"
            f"Arquivo: {caminho}\n"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Erro ao gerar PDF: {e}"


# ─── Endpoint Flask (adicione ao backend_agente.py) ──────────────────────────
# Cole isso no backend_agente.py para servir os PDFs gerados:
#
# from flask import send_file
# import glob
#
# @app.route("/api/pdf/<nome>")
# def servir_pdf(nome):
#     caminho = f"/tmp/pdfs_agente/{nome}"
#     if not os.path.exists(caminho):
#         return jsonify({"error": "PDF não encontrado"}), 404
#     return send_file(caminho, as_attachment=True, download_name=nome)
#
# @app.route("/api/pdfs", methods=["GET"])
# def listar_pdfs():
#     arquivos = glob.glob("/tmp/pdfs_agente/*.pdf")
#     return jsonify([os.path.basename(f) for f in sorted(arquivos)])


# ─── Teste rápido ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Resumo com tabela
    r = tool_gerar_pdf(
        tipo="resumo",
        titulo="Pipeline de CPU",
        topico="Organização de Computadores",
        secoes=[
            {
                "titulo": "O que é pipelining?",
                "conteudo": (
                    "Pipelining é uma técnica que permite executar múltiplas instruções "
                    "de forma sobreposta, dividindo a execução em estágios independentes.\n\n"
                    "O ganho de desempenho ideal é igual ao número de estágios, mas "
                    "hazards (de dados, controle e estruturais) reduzem esse ganho na prática."
                ),
            },
            {
                "titulo": "Hazards de pipeline",
                "conteudo": (
                    "Hazards são situações que impedem a próxima instrução de executar "
                    "no ciclo seguinte.\n\n"
                    "Hazard de dados: instrução depende do resultado de uma anterior ainda "
                    "no pipeline. Solução: forwarding ou stall (bolha).\n\n"
                    "Hazard de controle: branch muda o PC antes de sabermos o destino. "
                    "Solução: branch prediction ou delay slot."
                ),
            },
        ],
        tabela={
            "cabecalho": ["Estágio", "Sigla", "Função"],
            "linhas": [
                ["Instruction Fetch",  "IF",  "Busca a instrução na memória"],
                ["Instruction Decode", "ID",  "Decodifica e lê registradores"],
                ["Execute",            "EX",  "Executa operação na ALU"],
                ["Memory Access",      "MEM", "Acessa memória de dados"],
                ["Write Back",         "WB",  "Grava resultado no registrador"],
            ],
        },
    )
    print(r)

    # Lista de exercícios
    e = tool_gerar_pdf(
        tipo="exercicios",
        titulo="Exercícios — Sistemas de Numeração",
        topico="Representação de Dados",
        questoes=[
            {"enunciado": "Converta 255 (decimal) para binário e hexadecimal.",
             "gabarito": "11111111 em binário; FF em hexadecimal."},
            {"enunciado": "Qual é o valor decimal de 1010 1100 em binário com sinal (complemento de 2)?",
             "gabarito": "-84 (inverter bits → 0101 0011, somar 1 → 0101 0100 = 84, sinal negativo)."},
            {"enunciado": "Explique a diferença entre overflow e underflow em ponto flutuante IEEE 754.",
             "gabarito": "Overflow: expoente excede o máximo representável (+∞). Underflow: expoente é menor que o mínimo (número desnormalizado ou zero)."},
        ],
    )
    print(e)

    # Ficha de referência
    f = tool_gerar_pdf(
        tipo="ficha",
        titulo="Ficha — Hierarquia de Memória",
        topico="Arquitetura de Computadores",
        secoes=[
            {"titulo": "Registradores", "conteudo": "Dentro da CPU. < 1 ns. Dezenas de bytes."},
            {"titulo": "Cache L1",      "conteudo": "Dentro do core. ~1–4 ns. 32–64 KB."},
            {"titulo": "Cache L2",      "conteudo": "Próximo ao core. ~4–12 ns. 256 KB–1 MB."},
            {"titulo": "Cache L3",      "conteudo": "Compartilhada entre cores. ~30–50 ns. 4–64 MB."},
            {"titulo": "RAM (DRAM)",    "conteudo": "Fora do chip. ~60–100 ns. GBs."},
            {"titulo": "SSD / NVMe",   "conteudo": "Armazenamento não-volátil. ~0,1 ms. TBs."},
        ],
    )
    print(f)