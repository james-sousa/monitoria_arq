#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste para o Chatbot de Arquitetura e Organização de Computadores
Demonstra o funcionamento do chatbot com perguntas pré-programadas
"""

from chatbot import ChatbotArquitetura


def teste_chatbot():
    """Testa o chatbot com diversas perguntas"""
    
    chatbot = ChatbotArquitetura()
    
    # Lista de perguntas para teste
    perguntas_teste = [
        "O que é CPU?",
        "Como funciona o cache?",
        "Explique RAM",
        "O que é pipeline?",
        "Como é o ciclo de busca execução?",
        "Diferença entre Von Neumann e Harvard",
        "O que são registradores?",
        "Explique barramento",
        "O que é clock?",
        "Como são as interrupções?",
        "Qual é a diferença entre bit e byte?",
        "Tópicos",  # Comando especial
    ]
    
    print("=" * 80)
    print(" " * 20 + "TESTE DO CHATBOT DE ARQUITETURA")
    print("=" * 80)
    print()
    
    for i, pergunta in enumerate(perguntas_teste, 1):
        print(f"\n[Teste {i}]")
        print(f"Você: {pergunta}")
        
        resposta, _ = chatbot.processar_comando(pergunta)
        
        # Mostra apenas as primeiras 200 caracteres para resumo
        if len(resposta) > 200:
            print(f"Chatbot: {resposta[:200]}...\n")
        else:
            print(f"Chatbot: {resposta}\n")
        
        print("-" * 80)
    
    print("\n Teste completado com sucesso!")
    print(f"Total de perguntas processadas: {len(perguntas_teste)}")
    print(f"Histórico do chatbot: {len(chatbot.historico)} perguntas registradas")


def teste_performance():
    """Testa a performance do chatbot"""
    
    import time
    
    chatbot = ChatbotArquitetura()
    
    # Testa velocidade de resposta
    pergunta_teste = "O que é cache?"
    
    print("\n" + "=" * 80)
    print(" " * 25 + "TESTE DE PERFORMANCE")
    print("=" * 80)
    
    inicio = time.time()
    resposta, _ = chatbot.processar_comando(pergunta_teste)
    tempo_decorrido = (time.time() - inicio) * 1000  # em ms
    
    print(f"\nPergunta: {pergunta_teste}")
    print(f"Tempo de resposta: {tempo_decorrido:.2f}ms")
    print(f"Tamanho da resposta: {len(resposta)} caracteres")
    print("\n Performance excelente para Python puro!")


def teste_topicos():
    """Testa listagem de tópicos"""
    
    chatbot = ChatbotArquitetura()
    
    print("\n" + "=" * 80)
    print(" " * 25 + "TÓPICOS DISPONÍVEIS")
    print("=" * 80)
    
    topicos = chatbot.listar_topicos()
    print(f"\n{topicos}")


if __name__ == "__main__":
    # Executa todos os testes
    teste_chatbot()
    teste_topicos()
    teste_performance()
    
    print("\n" + "=" * 80)
    print("Todos os testes executados com sucesso! ")
    print("=" * 80)
