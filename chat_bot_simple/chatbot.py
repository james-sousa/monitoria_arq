#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chatbot para Arquitetura e Organização de Computadores
Um assistente simples em Python puro para tirar dúvidas sobre a disciplina
"""

import re
from typing import Dict, List, Tuple

class ChatbotArquitetura:
    """Chatbot especializado em Arquitetura e Organização de Computadores"""
    
    def __init__(self):
        """Inicializa o chatbot com base de conhecimento"""
        self.base_conhecimento = self._criar_base_conhecimento()
        self.historico = []
        
    def _criar_base_conhecimento(self) -> Dict[str, str]:
        """
        Cria a base de conhecimento sobre o assunto
        Estrutura: palavras-chave -> resposta
        """
        return {
            # CPU e Processador
            "cpu": """A CPU (Unidade Central de Processamento) é o "cérebro" do computador. 
Ela executa instruções do programa, controla todas as operações e coordena as atividades de todo o sistema.
Características principais:
- Busca instruções da memória
- Decodifica instruções
- Executa operações
- Armazena resultados""",

            "processador": """Um processador é sinônimo de CPU. É o componente que:
- Realiza operações matemáticas e lógicas
- Controla o fluxo de dados
- Executa programas
- Tem velocidade medida em GHz (gigahertz)
Quanto maior a frequência, mais instruções por segundo consegue executar.""",

            "registrador": """Registradores são memórias muito rápidas dentro da CPU que armazenam:
- Dados sendo processados
- Endereços de memória
- Estados da CPU
- Instruções em execução

São os tipos de memória mais rápidos do computador.""",

            "alu": """A ALU (Unidade Lógica e Aritmética) é responsável por:
- Operações aritméticas (+, -, *, /)
- Operações lógicas (AND, OR, NOT)
- Comparações
Trabalha com dados dos registradores.""",

            # Memória
            "memória": """A memória do computador se organiza em hierarquia:
1. REGISTRADORES - Mais rápidos, armazenam 64-256 bits
2. CACHE - Muito rápido, megabytes
3. RAM - Rápida, gigabytes, volátil
4. DISCO - Lento, muita capacidade, não volátil

Quanto maior a velocidade, menor a capacidade e mais cara.""",

            "ram": """RAM (Memória de Acesso Aleatório):
- Memória volátil (perde dados sem energia)
- Acesso aleatório em O(1)
- Usada durante execução de programas
- Mais rápida que disco, mais lenta que cache
- Capacidade típica: 4GB a 32GB""",

            "cache": """Cache é memória muito rápida entre CPU e RAM:
- L1: 32KB, dentro da CPU
- L2: 256KB, dentro da CPU
- L3: 8MB, compartilhada entre núcleos
Reduz tempo de acesso à RAM mantendo dados frequentes próximos.""",

            "disco": """Disco rígido ou SSD para armazenamento permanente:
- Não volátil (mantém dados sem energia)
- Muito mais lento que RAM
- Grande capacidade (terabytes)
- SSD é mais rápido que HD tradicional""",

            # Instruções e Ciclo
            "ciclo": """Ciclo de busca-execução (Fetch-Execute Cycle):
1. FETCH: Busca instrução na memória
2. DECODE: Decodifica a instrução
3. EXECUTE: Executa a operação
4. STORE: Armazena o resultado
Repetido bilhões de vezes por segundo.""",

            "instrução": """Uma instrução é uma operação elementar que a CPU executa:
- Tipo de operação (MOV, ADD, etc)
- Operandos (dados a operar)
- Modos de endereçamento (onde buscar dados)
Cada instrução leva ciclos de clock para executar.""",

            # Barramentos
            "barramento": """Barramento é o caminho de comunicação entre componentes:
- BARRAMENTO DE DADOS: Transfere dados (32, 64, 128 bits)
- BARRAMENTO DE ENDEREÇO: Identifica localização de memória
- BARRAMENTO DE CONTROLE: Sinais de controle
Velocidade medida em MHz ou GHz.""",

            "clock": """Clock é o sinal de sincronização do computador:
- Oscila entre 0 e 1
- Cadencia todas as operações
- Frequência em GHz
- Exemplo: 3.6 GHz = 3.6 bilhões de pulsos por segundo
Cada instrução leva múltiplos ciclos de clock.""",

            # Arquitetura
            "arquitetura": """Arquitetura de computadores estuda:
- Organização de componentes (CPU, memória, barramento)
- Conjunto de instruções (ISA)
- Modos de endereçamento
- Parallelismo (pipeline, superescala)
- Cache e gerência de memória""",

            "von neumann": """Arquitetura de Von Neumann (clássica):
- Memória única para dados e instruções
- Unidade de controle
- ALU
- Entrada/saída
- Programa armazenado em memória
A maioria dos computadores usa essa arquitetura.""",

            "harvard": """Arquitetura Harvard:
- Memória separada para dados e instruções
- Permite acesso simultâneo
- Mais rápida que Von Neumann
- Usada em microcontroladores e DSPs""",

            # Pipeline
            "pipeline": """Pipeline permite paralelismo ao dividir a execução em estágios:
1. FETCH (busca)
2. DECODE (decodifica)
3. EXECUTE (executa)
4. MEMORY (acesso memória)
5. WRITE (escreve resultado)

Múltiplas instruções em estágios diferentes simultaneamente.
Hazards podem causar travamentos.""",

            # Bit e Byte
            "bit": """BIT (Binary Digit) é a unidade menor de informação:
- Valor: 0 ou 1
- Representação: baixa tensão (0) ou alta tensão (1)
- Base para tudo em computadores digitais""",

            "byte": """BYTE são 8 bits:
- Unidade básica de endereçamento de memória
- Representa valores de 0 a 255 (sem sinal) ou -128 a 127 (com sinal)
- Usado para medir capacidade de armazenamento
1 KB = 1024 bytes
1 MB = 1024 KB
1 GB = 1024 MB""",

            # Endereçamento
            "endereçamento": """Modos de endereçamento especificam onde buscar operandos:
- IMEDIATO: valor na própria instrução
- DIRETO: endereço na memória
- INDIRETO: endereço em registrador
- INDEXADO: endereço + deslocamento
- RELATIVO: para instruções de salto""",

            # Interrupções
            "interrupção": """Interrupções são sinais que desviam a execução normal:
- Externas: dispositivos (teclado, disco)
- Internas: erro, divisão por zero
- Software: system calls

Processo:
1. CPU interrompe programa atual
2. Salva estado em pilha
3. Executa handler de interrupção
4. Restaura estado e retorna""",

            # Default
            "ajuda": """Comandos disponíveis:
- Digite perguntas naturais sobre o assunto
- 'sair' ou 'quit' para finalizar
- 'tópicos' para ver temas disponíveis

Tópicos principais:
CPU, Memória, Cache, RAM, Disco, Instruções, Clock, Pipeline,
Barramento, Arquitetura, Von Neumann, Harvard, Registrador, ALU,
Ciclo, Bit, Byte, Endereçamento, Interrupção
            """,
        }
    
    def _extrair_palavras_chave(self, texto: str) -> List[str]:
        """Extrai palavras-chave do texto do usuário"""
        # Converte para minúsculas e remove pontuação
        texto_limpo = re.sub(r'[^\w\s]', '', texto.lower())
        return texto_limpo.split()
    
    def _buscar_resposta(self, pergunta: str) -> str:
        """Busca a melhor resposta para a pergunta"""
        palavras_chave = self._extrair_palavras_chave(pergunta)
        
        # Busca por correspondência exata (chave da base de conhecimento)
        for palavra in palavras_chave:
            if palavra in self.base_conhecimento:
                return self.base_conhecimento[palavra]
        
        # Busca por similitude (contém a palavra)
        for palavra in palavras_chave:
            for chave, resposta in self.base_conhecimento.items():
                if palavra in chave or chave in palavra:
                    return resposta
        
        # Resposta padrão se não encontrar
        return self._resposta_padrao(palavras_chave)
    
    def _resposta_padrao(self, palavras_chave: List[str]) -> str:
        """Resposta quando não encontra correspondência"""
        if not palavras_chave:
            return "Por favor, faça uma pergunta sobre Arquitetura e Organização de Computadores."
        
        palavra = palavras_chave[0]
        return f"""Desculpe, não tenho informações específicas sobre '{palavra}'.

Tópicos que posso ajudar:
- CPU, Processador, Registrador, ALU
- Memória, RAM, Cache, Disco
- Instruções, Ciclo de busca-execução
- Clock, Barramento
- Arquitetura (Von Neumann, Harvard)
- Pipeline
- Bit, Byte
- Endereçamento
- Interrupções

Digite 'ajuda' para mais informações ou 'tópicos' para ver todos os temas."""
    
    def responder(self, pergunta: str) -> str:
        """Responde à pergunta do usuário"""
        if not pergunta.strip():
            return "Por favor, faça uma pergunta."
        
        resposta = self._buscar_resposta(pergunta)
        
        # Registra no histórico
        self.historico.append({
            'pergunta': pergunta,
            'resposta': resposta
        })
        
        return resposta
    
    def listar_topicos(self) -> str:
        """Lista todos os tópicos disponíveis"""
        topicos = sorted(self.base_conhecimento.keys())
        return "Tópicos disponíveis:\n" + "\n".join(f"- {t}" for t in topicos)
    
    def processar_comando(self, entrada: str) -> Tuple[str, bool]:
        """
        Processa a entrada do usuário
        Retorna: (resposta, deve_continuar)
        """
        entrada = entrada.strip()
        
        if entrada.lower() in ['sair', 'quit', 'exit']:
            return "Até logo! Continue estudando!", False
        
        if entrada.lower() in ['tópicos', 'topicos']:
            return self.listar_topicos(), True
        
        if entrada.lower() == 'ajuda':
            return self.base_conhecimento['ajuda'], True
        
        # Pergunta normal
        resposta = self.responder(entrada)
        return resposta, True


def main():
    """Função principal - loop do chatbot"""
    print("=" * 70)
    print("CHATBOT - ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES")
    print("=" * 70)
    print("\nOlá! Sou um assistente para tirar dúvidas sobre Arquitetura e")
    print("Organização de Computadores. Você pode fazer perguntas naturais.")
    print("\nDigite 'ajuda' para ver os comandos disponíveis")
    print("Digite 'sair' para finalizar a conversa\n")
    
    chatbot = ChatbotArquitetura()
    
    while True:
        try:
            pergunta = input("\nVocê: ").strip()
            
            if not pergunta:
                continue
            
            resposta, deve_continuar = chatbot.processar_comando(pergunta)
            
            print("\nChatbot:", resposta)
            
            if not deve_continuar:
                break
                
        except KeyboardInterrupt:
            print("\n\nConversa interrompida. Até logo!")
            break
        except Exception as e:
            print(f"Erro: {e}")
            continue


if __name__ == "__main__":
    main()
