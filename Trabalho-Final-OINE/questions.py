# questions.py
import random

# Estrutura principal: Um dicionário onde cada chave é o "Tema" ou a "Fase" do Boss.
# Você pode adicionar até 100 perguntas dentro de cada colchetes [] sem problemas!
QUESTION_BANK = {
    "Pilha": [
        {
            "pergunta": "Qual é a principal regra de funcionamento de uma Pilha (Stack)?",
            "opcoes": ["A) LIFO (Last In, First Out)", "B) FIFO (First In, First Out)", "C) Aleatório", "D) LILO (Last In, Last Out)"],
            "correta": 0 # Índice da resposta correta (0 = A, 1 = B, 2 = C, 3 = D)
        },
        {
            "pergunta": "Qual operação é usada para inserir um elemento no topo da Pilha?",
            "opcoes": ["A) Pop", "B) Push", "C) Enqueue", "D) Insert"],
            "correta": 1
        },
        {
            "pergunta": "Qual dos exemplos do mundo real melhor representa uma Pilha?",
            "opcoes": ["A) Fila do banco", "B) Histórico do navegador (Voltar)", "C) Senhas de atendimento", "D) Fila do supermercado"],
            "correta": 1
        },
        {
            "pergunta": "Se fizermos Push(1), Push(2), Push(3) e um Pop(). Qual valor é removido?",
            "opcoes": ["A) 1", "B) 2", "C) 3", "D) Nenhum"],
            "correta": 2
        }
    ],
    
    "Fila": [
        {
            "pergunta": "Qual é a principal regra de funcionamento de uma Fila (Queue)?",
            "opcoes": ["A) LIFO (Last In, First Out)", "B) LILO (Last In, Last Out)", "C) FIFO (First In, First Out)", "D) FILO (First In, Last Out)"],
            "correta": 2
        },
        {
            "pergunta": "Como se chama a operação de remover um elemento de uma Fila?",
            "opcoes": ["A) Pop", "B) Dequeue", "C) Enqueue", "D) Remove"],
            "correta": 1
        },
        {
            "pergunta": "Qual estrutura de dados é ideal para gerenciar impressões em uma impressora?",
            "opcoes": ["A) Pilha", "B) Árvore", "C) Grafo", "D) Fila"],
            "correta": 3
        }
    ],

    "Arvore": [
        {
            "pergunta": "Em uma Árvore, como é chamado o elemento que não possui 'filhos'?",
            "opcoes": ["A) Raiz (Root)", "B) Nó (Node)", "C) Folha (Leaf)", "D) Galho (Branch)"],
            "correta": 2
        },
        {
            "pergunta": "Qual a principal vantagem de uma Árvore Binária de Busca (BST)?",
            "opcoes": ["A) Pesquisa mais rápida que arrays não ordenados", "B) Ocupa menos memória", "C) Funciona como uma Fila", "D) Não usa ponteiros"],
            "correta": 0
        }
    ]
}

def get_random_question(fase_atual):
    """
    Busca todas as perguntas da fase (ex: 'Pilha') e retorna UMA pergunta aleatória.
    """
    if fase_atual in QUESTION_BANK:
        lista_de_perguntas = QUESTION_BANK[fase_atual]
        # random.choice escolhe um item aleatório da lista
        return random.choice(lista_de_perguntas)
    else:
        # Retorno de segurança caso a fase seja digitada errada
        return {
            "pergunta": "Erro: Fase não encontrada no banco de dados.",
            "opcoes": ["A) -", "B) -", "C) -", "D) -"],
            "correta": 0
        }