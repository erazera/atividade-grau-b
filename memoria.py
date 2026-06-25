"""
memoria.py — Estruturas de Dados

Contém as estruturas do sistema:
  • Memória RAM — lista de frames
  • Fila LRU — controle de páginas por ordem de uso
  • Frames livres 
  • Contadores — estatísticas de hits e page faults
"""

from config import TOTAL_FRAMES

# Memória RAM

# Lista de 8 frames. Cada posição armazena o conteúdo da página carregada. Inicialmente todos os frames estão vazios
memoria_principal = [None] * TOTAL_FRAMES

# Tabela de Páginas

# Estrutura: { processo_id: { numero_pagina: { "frame": int, "presente": bool } } }
tabelas_de_paginas = {}

# Fila LRU

# Lista de tuplas (processo_id, numero_pagina)
fila_lru = []

# Frames Livres

# Lista com os índices dos frames disponíveis: [0, 1, 2, ..., 7].
frames_livres = list(range(TOTAL_FRAMES))

# Contadores para Estatísticas
contadores = {"hits": 0, "page_faults": 0, "total": 0}
