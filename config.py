"""
config.py — Constantes

"""

TAMANHO_MEMORIA_VIRTUAL   = 1 * 1024 * 1024   
TAMANHO_MEMORIA_PRINCIPAL = 64 * 1024          
TAMANHO_PAGINA            = 8 * 1024           


TOTAL_PAGINAS = TAMANHO_MEMORIA_VIRTUAL  // TAMANHO_PAGINA   # 128 páginas
TOTAL_FRAMES  = TAMANHO_MEMORIA_PRINCIPAL // TAMANHO_PAGINA  # 8 frames


PAUSA_ENTRE_INSTRUCOES = 1.5  # para facilitar o acompanhamento no vídeo
