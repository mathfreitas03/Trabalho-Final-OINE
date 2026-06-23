# questions.py
import random
import copy

QUESTION_BANK = {
    "Pilha": [
        {"pergunta": "Qual é a principal regra de funcionamento de uma Pilha?", "opcoes": ["A) LIFO (Last In, First Out)", "B) FIFO (First In, First Out)", "C) Aleatório", "D) LILO"], "correta": 0},
        {"pergunta": "Qual operação insere um elemento no topo da Pilha?", "opcoes": ["A) Pop", "B) Push", "C) Enqueue", "D) Insert"], "correta": 1},
        {"pergunta": "Qual operação remove um elemento do topo da Pilha?", "opcoes": ["A) Push", "B) Dequeue", "C) Pop", "D) Remove"], "correta": 2},
        {"pergunta": "Qual ponteiro controla o elemento acessível em uma Pilha?", "opcoes": ["A) Base", "B) Front", "C) Rear", "D) Top (Topo)"], "correta": 3},
        {"pergunta": "O que acontece ao tentar remover de uma pilha vazia?", "opcoes": ["A) Overflow", "B) Underflow", "C) Deadlock", "D) Loop infinito"], "correta": 1},
        {"pergunta": "O que acontece ao tentar inserir em uma pilha cheia?", "opcoes": ["A) Underflow", "B) Crash", "C) Overflow", "D) Override"], "correta": 2},
        {"pergunta": "Qual exemplo real representa uma Pilha?", "opcoes": ["A) Fila de banco", "B) Navegação 'Voltar' do Browser", "C) Senhas médicas", "D) Buffer de vídeo"], "correta": 1},
        {"pergunta": "Qual atalho de teclado simula o conceito de Pilha?", "opcoes": ["A) Ctrl+C (Copiar)", "B) Ctrl+V (Colar)", "C) Ctrl+Z (Desfazer)", "D) Ctrl+F (Buscar)"], "correta": 2},
        {"pergunta": "Push(1), Push(2), Push(3), Pop(). Qual número saiu?", "opcoes": ["A) 1", "B) 2", "C) 3", "D) Nenhum"], "correta": 2},
        {"pergunta": "Push(A), Push(B), Pop(), Push(C). Qual é o topo agora?", "opcoes": ["A) A", "B) B", "C) C", "D) Vazio"], "correta": 2},
        {"pergunta": "Qual estrutura na memória RAM funciona como uma Pilha?", "opcoes": ["A) Heap", "B) Call Stack (Pilha de Execução)", "C) Registradores", "D) Cache"], "correta": 1},
        {"pergunta": "Uma Pilha permite acesso aleatório aos seus elementos?", "opcoes": ["A) Sim, pelo índice", "B) Sim, pela chave", "C) Não, apenas ao topo", "D) Não, apenas à base"], "correta": 2},
        {"pergunta": "Na avaliação de qual notação matemática as pilhas são muito usadas?", "opcoes": ["A) Notação Polonesa (Posfixa)", "B) Frações", "C) Matrizes", "D) Logaritmos"], "correta": 0},
        {"pergunta": "Qual a complexidade de tempo (Big-O) para um Pop() comum?", "opcoes": ["A) O(n)", "B) O(n log n)", "C) O(1)", "D) O(n^2)"], "correta": 2},
        {"pergunta": "Qual algoritmo de busca em grafos utiliza Pilha?", "opcoes": ["A) BFS (Largura)", "B) Dijkstra", "C) DFS (Profundidade)", "D) A*"], "correta": 2},
        {"pergunta": "Para verificar se parênteses estão balanceados no código, usamos:", "opcoes": ["A) Fila", "B) Grafo", "C) Pilha", "D) Árvore"], "correta": 2},
        {"pergunta": "Em Python, qual estrutura nativa é usada frequentemente como Pilha?", "opcoes": ["A) Tuple", "B) Dictionary", "C) Set", "D) List (usando append e pop)"], "correta": 3},
        {"pergunta": "Se uma Pilha tem tamanho máximo 5, no 6º push ocorrerá:", "opcoes": ["A) Expansão automática sempre", "B) Underflow", "C) Overflow", "D) Substituição da base"], "correta": 2},
        {"pergunta": "Uma função recursiva que chama a si mesma infinitamente causa:", "opcoes": ["A) Stack Overflow", "B) Memory Leak", "C) Null Pointer", "D) Syntax Error"], "correta": 0},
        {"pergunta": "O elemento inserido primeiro numa pilha será retirado...", "opcoes": ["A) Primeiro", "B) Aleatoriamente", "C) No meio", "D) Por último"], "correta": 3},
        {"pergunta": "Qual método espia o topo sem removê-lo?", "opcoes": ["A) See()", "B) Peek() / Top()", "C) Look()", "D) Check()"], "correta": 1},
        {"pergunta": "Para inverter a palavra 'ROMA' usando pilha, o primeiro pop será:", "opcoes": ["A) R", "B) O", "C) M", "D) A"], "correta": 3},
        {"pergunta": "Pilhas são estruturas de dados de qual categoria?", "opcoes": ["A) Não-lineares", "B) Lineares", "C) Relacionais", "D) Dinâmicas estritas"], "correta": 1},
        {"pergunta": "Como é chamada uma pilha que não tem limite fixo de tamanho?", "opcoes": ["A) Estática", "B) Dinâmica", "C) Abstrata", "D) Circular"], "correta": 1},
        {"pergunta": "Push(10), Push(20), Pop(), Pop(), Pop(). O que ocorre no 3º Pop?", "opcoes": ["A) Sai o 10", "B) Underflow", "C) Overflow", "D) Retorna 0"], "correta": 1},
        {"pergunta": "A Torre de Hanói é tradicionalmente resolvida usando o conceito de:", "opcoes": ["A) Filas", "B) Matrizes", "C) Grafos", "D) Pilhas"], "correta": 3},
        {"pergunta": "Em uma pilha estática implementada com vetor, a base fica no índice:", "opcoes": ["A) N", "B) -1", "C) 0", "D) N-1"], "correta": 2},
        {"pergunta": "Qual destas NÃO é uma operação padrão de Pilha?", "opcoes": ["A) Push", "B) Pop", "C) Peek", "D) Sort (Ordenar)"], "correta": 3},
        {"pergunta": "Qual destas variáveis é dispensável ao gerenciar uma pilha simples?", "opcoes": ["A) Tamanho", "B) Topo", "C) Fim (Rear)", "D) Array de dados"], "correta": 2},
        {"pergunta": "LIFO é um acrônimo para:", "opcoes": ["A) Last In, First Out", "B) List In, File Out", "C) Last Index, First Option", "D) Linear Input, Fast Output"], "correta": 0}
    ],
    
    "Fila": [
        {"pergunta": "Qual é a principal regra de funcionamento de uma Fila?", "opcoes": ["A) LIFO", "B) LILO", "C) FIFO (First In, First Out)", "D) Aleatório"], "correta": 2},
        {"pergunta": "Qual operação insere um elemento em uma Fila?", "opcoes": ["A) Push", "B) Enqueue (Enfileirar)", "C) Pop", "D) Shift"], "correta": 1},
        {"pergunta": "Qual operação remove um elemento de uma Fila?", "opcoes": ["A) Pop", "B) Dequeue (Desenfileirar)", "C) Delete", "D) Erase"], "correta": 1},
        {"pergunta": "Em uma fila simples, novos elementos entram por onde?", "opcoes": ["A) Frente (Front)", "B) Meio", "C) Trás (Rear)", "D) Aleatório"], "correta": 2},
        {"pergunta": "Em uma fila simples, de onde os elementos são removidos?", "opcoes": ["A) Frente (Front)", "B) Trás (Rear)", "C) Meio", "D) O maior valor"], "correta": 0},
        {"pergunta": "Qual é o exemplo mais clássico do mundo real de uma Fila?", "opcoes": ["A) Livros em uma caixa", "B) Atendimento no banco", "C) Ctrl+Z do Word", "D) Árvore genealógica"], "correta": 1},
        {"pergunta": "Qual processo de Sistema Operacional usa Fila?", "opcoes": ["A) Call Stack", "B) Escalonamento Round-Robin", "C) Pilha de Execução", "D) Paginação Aleatória"], "correta": 1},
        {"pergunta": "Enqueue(A), Enqueue(B), Dequeue(). Quem saiu?", "opcoes": ["A) B", "B) A", "C) Ambos", "D) Nenhum"], "correta": 1},
        {"pergunta": "Qual variação de fila evita o desperdício de espaço do vetor?", "opcoes": ["A) Fila Dupla", "B) Fila de Prioridade", "C) Fila Circular", "D) Fila Abstrata"], "correta": 2},
        {"pergunta": "Em um DEQUE (Fila Duplamente Terminada), onde podemos inserir?", "opcoes": ["A) Só na frente", "B) Só atrás", "C) No meio", "D) Na frente e atrás"], "correta": 3},
        {"pergunta": "Na Fila de Prioridade, qual elemento é removido primeiro?", "opcoes": ["A) O mais antigo", "B) O mais novo", "C) O de maior prioridade", "D) O menor valor sempre"], "correta": 2},
        {"pergunta": "Fila é uma estrutura de dados Linear ou Não-Linear?", "opcoes": ["A) Linear", "B) Não-Linear", "C) Circular pura", "D) Hierárquica"], "correta": 0},
        {"pergunta": "Qual algoritmo de busca usa uma Fila em sua base?", "opcoes": ["A) DFS (Profundidade)", "B) BFS (Largura)", "C) Backtracking", "D) Divisão e Conquista"], "correta": 1},
        {"pergunta": "No Spooler de Impressão, o 3º arquivo mandado será impresso em qual ordem?", "opcoes": ["A) 1º", "B) 3º", "C) Último", "D) Aleatório"], "correta": 1},
        {"pergunta": "Se `Front == Rear` em uma fila estática circular comum, ela está:", "opcoes": ["A) Cheia", "B) Pela metade", "C) Vazia", "D) Corrompida"], "correta": 2},
        {"pergunta": "Enqueue(1), Enqueue(2), Enqueue(3), Dequeue(), Dequeue(). Resta?", "opcoes": ["A) 1", "B) 2", "C) 3", "D) Nada"], "correta": 2},
        {"pergunta": "Em Python, usar uma lista simples como Fila (pop(0)) é ruim porque:", "opcoes": ["A) É O(n) e lento", "B) É proibido", "C) Causa Overflow", "D) Só aceita strings"], "correta": 0},
        {"pergunta": "Qual módulo do Python fornece uma fila eficiente (Deque)?", "opcoes": ["A) math", "B) sys", "C) collections", "D) os"], "correta": 2},
        {"pergunta": "O que causa um Overflow na Fila?", "opcoes": ["A) Tentar remover com fila vazia", "B) Tentar inserir com fila cheia", "C) Fila infinita", "D) Bug no Rear"], "correta": 1},
        {"pergunta": "O que causa um Underflow na Fila?", "opcoes": ["A) Inserir com fila cheia", "B) Imprimir a fila", "C) Tentar remover de fila vazia", "D) Limpar a fila"], "correta": 2},
        {"pergunta": "FIFO é o acrônimo para:", "opcoes": ["A) First In, Fast Out", "B) First In, First Out", "C) Fast In, First Out", "D) Final In, First Out"], "correta": 1},
        {"pergunta": "Em filas de atendimento de telemarketing, usa-se estrutura tipo:", "opcoes": ["A) Pilha", "B) Grafo", "C) Árvore", "D) Fila (ACD)"], "correta": 3},
        {"pergunta": "A operação Peek/Front numa fila serve para:", "opcoes": ["A) Remover o primeiro", "B) Olhar o último", "C) Olhar o primeiro sem remover", "D) Esvaziar a fila"], "correta": 2},
        {"pergunta": "Num DEQUE, a operação 'PopRight' assemelha-se a remover de uma:", "opcoes": ["A) Pilha", "B) Fila simples", "C) Árvore AVL", "D) Lista vazia"], "correta": 0},
        {"pergunta": "Se o Rear apontar para o limite máximo do array e Front para 0, a fila está:", "opcoes": ["A) Vazia", "B) Quebrada", "C) Cheia", "D) Negativa"], "correta": 2},
        {"pergunta": "Uma fila implementada com Listas Encadeadas tem limite de tamanho?", "opcoes": ["A) Sim, 100", "B) Não, depende da RAM", "C) Sim, 255", "D) Só aceita inteiros"], "correta": 1},
        {"pergunta": "Ao desenfileirar em uma fila encadeada, qual ponteiro muda?", "opcoes": ["A) Rear", "B) Front", "C) Ambos", "D) O meio"], "correta": 1},
        {"pergunta": "Ao enfileirar em uma fila encadeada, qual ponteiro muda (normalmente)?", "opcoes": ["A) Front", "B) Rear", "C) Raiz", "D) Top"], "correta": 1},
        {"pergunta": "Em processamento de streaming de vídeo de rede, os pacotes ficam em uma:", "opcoes": ["A) Pilha de pacotes", "B) Fila (Buffer)", "C) Árvore Binária", "D) Matriz 3D"], "correta": 1},
        {"pergunta": "Fila é frequentemente usada para sincronização de tarefas assíncronas?", "opcoes": ["A) Nunca", "B) Só em C++", "C) Sim (Ex: Message Queues)", "D) Apenas no frontend"], "correta": 2}
    ],

    "Arvore": [
        {"pergunta": "Em uma Árvore, o que é o Nó Raiz (Root)?", "opcoes": ["A) O nó mais profundo", "B) O nó no topo sem pai", "C) Qualquer folha", "D) A conexão (Aresta)"], "correta": 1},
        {"pergunta": "Como é chamado o nó que não possui nenhum filho?", "opcoes": ["A) Galho", "B) Raiz", "C) Irmão", "D) Folha (Leaf)"], "correta": 3},
        {"pergunta": "O que define uma Árvore Binária?", "opcoes": ["A) Só tem números binários", "B) Max 2 filhos por nó", "C) 10 filhos por nó", "D) Não possui folhas"], "correta": 1},
        {"pergunta": "Na BST (Binary Search Tree), os valores menores que a raiz vão para:", "opcoes": ["A) Subárvore Direita", "B) Subárvore Esquerda", "C) O nó Folha", "D) A raiz"], "correta": 1},
        {"pergunta": "Na BST (Binary Search Tree), os valores maiores que a raiz vão para:", "opcoes": ["A) Subárvore Direita", "B) Subárvore Esquerda", "C) Subárvore Central", "D) A base"], "correta": 0},
        {"pergunta": "O que é a 'Altura' de uma árvore?", "opcoes": ["A) O número total de nós", "B) O maior caminho da raiz até uma folha", "C) A quantidade de folhas", "D) O grau máximo"], "correta": 1},
        {"pergunta": "A travessia In-Order em uma BST resulta em elementos:", "opcoes": ["A) Aleatórios", "B) Ordem decrescente", "C) Ordem crescente (Ordenados)", "D) Em formato de Pilha"], "correta": 2},
        {"pergunta": "Qual o pior caso de tempo de busca numa BST desbalanceada?", "opcoes": ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n^2)"], "correta": 2},
        {"pergunta": "Qual a vantagem de uma Árvore AVL?", "opcoes": ["A) Ela se auto-balanceia", "B) Ocupa 0 bytes", "C) Funciona como Pilha", "D) Aceita infinitos filhos"], "correta": 0},
        {"pergunta": "Nós que compartilham o mesmo pai são chamados de:", "opcoes": ["A) Tios", "B) Raízes", "C) Descendentes", "D) Irmãos (Siblings)"], "correta": 3},
        {"pergunta": "Árvore é uma estrutura linear ou não-linear?", "opcoes": ["A) Linear", "B) Não-linear (Hierárquica)", "C) Matricial", "D) Unidimensional"], "correta": 1},
        {"pergunta": "Qual travessia visita Raiz -> Esquerda -> Direita?", "opcoes": ["A) Pre-order", "B) In-order", "C) Post-order", "D) Level-order"], "correta": 0},
        {"pergunta": "Qual travessia visita Esquerda -> Direita -> Raiz?", "opcoes": ["A) Pre-order", "B) In-order", "C) Post-order", "D) Level-order"], "correta": 2},
        {"pergunta": "Qual exemplo clássico de software utiliza árvores?", "opcoes": ["A) Sistema de Arquivos e Pastas", "B) Histórico do Navegador", "C) Fila do Banco", "D) Spooler de Impressão"], "correta": 0},
        {"pergunta": "O que é uma Árvore Binária Completa?", "opcoes": ["A) Não tem folhas", "B) Todos os níveis cheios, último da esq. pra dir.", "C) Só tem raiz", "D) Cada nó tem 3 filhos"], "correta": 1},
        {"pergunta": "Qual estrutura baseia a implementação técnica do Heap?", "opcoes": ["A) Lista Ligada", "B) Árvore Binária Quase Completa", "C) Grafo Cíclico", "D) Fila Circular"], "correta": 1},
        {"pergunta": "O DOM (Document Object Model) de uma página HTML é uma:", "opcoes": ["A) Pilha", "B) Tabela Hash", "C) Árvore", "D) Fila"], "correta": 2},
        {"pergunta": "Árvore Rubro-Negra (Red-Black) é um tipo de:", "opcoes": ["A) Fila Dupla", "B) Grafo Desconexo", "C) Árvore Auto-Balanceada", "D) Banco de dados SQL"], "correta": 2},
        {"pergunta": "Ao buscar o valor 10 numa BST cuja raiz é 20, o primeiro passo é:", "opcoes": ["A) Ir para Direita", "B) Ir para Esquerda", "C) Retornar erro", "D) Excluir a raiz"], "correta": 1},
        {"pergunta": "Quantos pais no máximo um nó (que não seja a raiz) pode ter em uma árvore?", "opcoes": ["A) 2", "B) 3", "C) Múltiplos", "D) 1"], "correta": 3},
        {"pergunta": "O que caracteriza um Grafo Cíclico e o difere de uma Árvore?", "opcoes": ["A) Possui nós", "B) Possui arestas", "C) Contém ciclos (loops fechados)", "D) Possui raízes múltiplas"], "correta": 2},
        {"pergunta": "No nível 0 de uma árvore (a raiz), qual o número máximo de nós?", "opcoes": ["A) 0", "B) 1", "C) 2", "D) Infinito"], "correta": 1},
        {"pergunta": "O nível máximo de uma árvore binária perfeita com altura H tem quantos nós?", "opcoes": ["A) 2^H", "B) H+1", "C) H^2", "D) 2H"], "correta": 0},
        {"pergunta": "Remover uma folha de uma BST afeta os outros nós?", "opcoes": ["A) Sim, embaralha a árvore toda", "B) Não, é a remoção mais simples", "C) Causa underflow fatal", "D) Aumenta a altura"], "correta": 1},
        {"pergunta": "Uma árvore cujos nós podem ter mais de 2 filhos é chamada de:", "opcoes": ["A) Árvore Binária", "B) Árvore AVL", "C) Árvore N-ária", "D) Árvore de Pilha"], "correta": 2},
        {"pergunta": "A travessia por níveis (Level-order) utiliza qual estrutura como auxiliar?", "opcoes": ["A) Pilha", "B) Fila", "C) Árvore Secundária", "D) Tabela Hash"], "correta": 1},
        {"pergunta": "Em um Min-Heap, o menor elemento de todos sempre está:", "opcoes": ["A) Em uma folha", "B) Na subárvore direita", "C) Na Raiz", "D) No último nível"], "correta": 2},
        {"pergunta": "Em um Max-Heap, o maior elemento sempre está:", "opcoes": ["A) Na Raiz", "B) Na folha", "C) Na subárvore esquerda", "D) No meio"], "correta": 0},
        {"pergunta": "Para buscar dados espaciais (Ex: Mapas 2D), qual árvore é comum?", "opcoes": ["A) BST", "B) Red-Black Tree", "C) Quadtree", "D) Árvore AVL"], "correta": 2},
        {"pergunta": "Em Bancos de Dados SQL, índices frequentemente usam qual variação de árvore?", "opcoes": ["A) B-Tree / B+ Tree", "B) Binary Tree simples", "C) Árvore Sintática", "D) Trie"], "correta": 0}
    ]
}

# Esse dicionário interno é quem vai gerenciar as perguntas que ainda não foram feitas!
_current_pool = {}

def get_random_question(fase_atual):
    """
    Busca as perguntas da fase. Se uma pergunta for sorteada, ela não repete 
    até que todas as 30 perguntas daquela fase tenham se esgotado.
    """
    global _current_pool
    
    # 1. Se a fase nunca foi jogada ou o pool dela secou, nós recarregamos!
    if fase_atual not in _current_pool or len(_current_pool[fase_atual]) == 0:
        if fase_atual in QUESTION_BANK:
            # copy.deepcopy cria uma lista independente para não apagar do banco original
            _current_pool[fase_atual] = copy.deepcopy(QUESTION_BANK[fase_atual])
        else:
            return {
                "pergunta": f"Erro: Fase '{fase_atual}' não encontrada no banco.",
                "opcoes": ["A) -", "B) -", "C) -", "D) -"],
                "correta": 0
            }
            
    # 2. Sorteia uma pergunta dentre as que SOBRARAM no pool
    pergunta_sorteada = random.choice(_current_pool[fase_atual])
    
    # 3. Remove a pergunta sorteada do pool para ela não cair de novo
    _current_pool[fase_atual].remove(pergunta_sorteada)
    
    # 4. Envia para a tela do jogo
    return pergunta_sorteada