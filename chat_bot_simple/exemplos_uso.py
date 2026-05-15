#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplo de Uso do Chatbot em Scripts Python
Mostra como integrar o chatbot em outras aplicações
"""

from chatbot import ChatbotArquitetura


def exemplo_uso_basico():
    """Exemplo 1: Uso básico"""
    print("=" * 70)
    print("EXEMPLO 1: Uso Básico")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    resposta = chatbot.responder("O que é CPU?")
    print(f"\nPergunta: O que é CPU?")
    print(f"Resposta:\n{resposta}\n")


def exemplo_multiplas_perguntas():
    """Exemplo 2: Processar múltiplas perguntas"""
    print("=" * 70)
    print("EXEMPLO 2: Múltiplas Perguntas")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    perguntas = [
        "Como funciona a memória cache?",
        "O que é pipeline?",
        "Explique Von Neumann"
    ]
    
    for pergunta in perguntas:
        resposta, _ = chatbot.processar_comando(pergunta)
        print(f"\n {pergunta}")
        print(f"   {resposta[:100]}...\n")


def exemplo_com_historico():
    """Exemplo 3: Acessar histórico"""
    print("=" * 70)
    print("EXEMPLO 3: Histórico de Perguntas")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    chatbot.responder("O que é CPU?")
    chatbot.responder("Como funciona RAM?")
    chatbot.responder("Explique cache")
    
    print(f"\nTotal de perguntas registradas: {len(chatbot.historico)}\n")
    
    for i, item in enumerate(chatbot.historico, 1):
        print(f"Pergunta {i}: {item['pergunta']}")
        print(f"Resposta (primeiros 80 chars): {item['resposta'][:80]}...\n")


def exemplo_tratamento_erros():
    """Exemplo 4: Tratamento de perguntas não conhecidas"""
    print("=" * 70)
    print("EXEMPLO 4: Perguntas Desconhecidas")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    perguntas_desconhecidas = [
        "Qual é a capital da França?",
        "Como fazer bolo?",
        "Explique fotossíntese",
        "xyz123abc"
    ]
    
    for pergunta in perguntas_desconhecidas:
        resposta, _ = chatbot.processar_comando(pergunta)
        print(f"\n Pergunta: {pergunta}")
        print(f"   {resposta[:80]}...\n")


def exemplo_listar_topicos():
    """Exemplo 5: Listar todos os tópicos"""
    print("=" * 70)
    print("EXEMPLO 5: Listando Tópicos Disponíveis")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    topicos = chatbot.listar_topicos()
    print(f"\n{topicos}\n")


def exemplo_busca_avancada():
    """Exemplo 6: Usando busca avançada"""
    print("=" * 70)
    print("EXEMPLO 6: Análise de Resposta")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    pergunta = "Como funciona o processador?"
    resposta, deve_continuar = chatbot.processar_comando(pergunta)
    
    print(f"\nPergunta: {pergunta}")
    print(f"Deve continuar: {deve_continuar}")
    print(f"Tamanho da resposta: {len(resposta)} caracteres")
    print(f"Número de linhas: {len(resposta.split(chr(10)))}")
    print(f"\nResposta:\n{resposta}\n")


def criar_resumo_resposta(resposta: str, max_chars: int = 150) -> str:
    """Função utilitária para resumir respostas"""
    if len(resposta) <= max_chars:
        return resposta
    return resposta[:max_chars].rstrip() + "..."


def exemplo_formatacao():
    """Exemplo 7: Formatação de respostas"""
    print("=" * 70)
    print("EXEMPLO 7: Formatando Respostas para Diferentes Contextos")
    print("=" * 70)
    
    chatbot = ChatbotArquitetura()
    
    pergunta = "O que é CPU?"
    resposta, _ = chatbot.processar_comando(pergunta)
    
    # Resumo curto
    resumo = criar_resumo_resposta(resposta, 100)
    print(f"\n🔹 Resumo curto:\n{resumo}\n")
    
    # Resposta completa
    print(f"🔹 Resposta completa:\n{resposta}\n")
    
    # Formatado como lista
    print("🔹 Pontos principais:")
    for linha in resposta.split('\n'):
        if linha.strip():
            print(f"   • {linha.strip()}")


def main():
    """Executa todos os exemplos"""
    
    # Descomente os exemplos que deseja executar
    
    exemplo_uso_basico()
    print("\n")
    
    exemplo_multiplas_perguntas()
    print("\n")
    
    exemplo_com_historico()
    print("\n")
    
    exemplo_tratamento_erros()
    print("\n")
    
    exemplo_listar_topicos()
    print("\n")
    
    exemplo_busca_avancada()
    print("\n")
    
    exemplo_formatacao()
    
    print("\n" + "=" * 70)
    print("Todos os exemplos executados com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
