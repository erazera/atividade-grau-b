"""
processos.py:
  • Os processos lógicos (id + tamanho)
  • A lista de instruções que o programa vai seguir
"""

def definir_processos():
    """
    Cria os processos lógicos do simulador
    """
    processos = [
        {"id": "A", "tamanho": 40 * 1024},  # 5 páginas
        {"id": "B", "tamanho": 32 * 1024},  # 4 páginas
    ]
    return processos


def definir_instrucoes():
    """
    Lista fixa

    Cada instrução é uma tupla: (processo_id, endereco_virtual)

    - Fase 1: Carregamento dos frames 
    - Fase 2: Acessos gerando HITs
    - Fase 3: Estouro da memória, fazendo o algortitmo LRU agir
    """
    instrucoes = [
        # Fase 1: 
        # Cada acesso a uma nova página gera um page fault porque a RAM está vazia

        ("A", 0),          
        ("A", 8192),      
        ("B", 0),          
        ("B", 8200),       
        ("A", 16384),      
        ("A", 24576),      
        ("B", 16384),      
        ("B", 24576),      

        # Enchemos a memória
        # Fila LRU: [A.Pg0, A.Pg1, B.Pg0, B.Pg1, A.Pg2, A.Pg3, B.Pg2, B.Pg3]

        # Fase 2
        # Acessar páginas que já estão na RAM

        ("A", 100),        
        ("B", 8500),       
        ("A", 16500),     

        ("A", 32768),      
        ("B", 100),        

        ("A", 9000),       

        ("B", 24600),      
        ("A", 500),        
    ]
    return instrucoes
