"""
mmu.py: Memory Management Unit 

Contém toda a lógica para o gerenciamento da memória virtual:
  • Inicialização de processos e suas tabelas de páginas
  • Decomposição de endereços virtuais
  • Tradução de endereço virtual para endereço físico
  • Detecção e tratamento de Page Fault
  • Algoritmo de substituição LRU

"""

import time

from config import TAMANHO_PAGINA, TOTAL_FRAMES, PAUSA_ENTRE_INSTRUCOES
from memoria import (
    memoria_principal,
    tabelas_de_paginas,
    fila_lru,
    frames_livres,
    contadores,
)

def gerar_conteudo_pagina(processo_id, numero_pagina):

    return f"[Dados do Processo {processo_id} | Página {numero_pagina}]"

# Inicialização de processos

def inicializar_processo(processo_id, tamanho_bytes):

    paginas_necessarias = (tamanho_bytes + TAMANHO_PAGINA - 1) // TAMANHO_PAGINA

    tabela = {}
    for pagina in range(paginas_necessarias):
        tabela[pagina] = {"frame": None, "presente": False}

    tabelas_de_paginas[processo_id] = tabela

    print(f"Processo {processo_id} criado: {tamanho_bytes} bytes "
          f"-> {paginas_necessarias} página(s) virtual(is)")

# Decomposição de endereço virtual

def decompor_endereco_virtual(endereco_virtual):
    """         
    Exemplo com página de 8 KB
      Endereço 20000  ->  Página 2, Offset 3616
    """
    numero_pagina = endereco_virtual // TAMANHO_PAGINA
    offset        = endereco_virtual %  TAMANHO_PAGINA
    return numero_pagina, offset


# Algoritmo LRU

def atualizar_fila_lru(processo_id, numero_pagina):

    chave = (processo_id, numero_pagina)
    if chave in fila_lru:
        fila_lru.remove(chave)
    fila_lru.append(chave)


def substituir_pagina_lru():
    # A página LRU é a primeira da fila
    proc_vitima, pag_vitima = fila_lru.pop(0)

    # Localiza o frame que ela ocupava
    entrada_vitima = tabelas_de_paginas[proc_vitima][pag_vitima]
    frame_liberado = entrada_vitima["frame"]

    # Marca a página como ausente na tabela de páginas
    entrada_vitima["presente"] = False
    entrada_vitima["frame"]    = None

    # Limpa o conteúdo do frame na memória principal
    memoria_principal[frame_liberado] = None

    print(f"LRU: Página {pag_vitima} do Processo {proc_vitima} "
          f"removida do Frame {frame_liberado}")

    return frame_liberado


# Carregamento de páginas

def carregar_pagina(processo_id, numero_pagina):
    """
    1. Se tem frame livre, usa o primeiro disponível
    2. Se a memória está cheia, usa o algoritmo LRU
    3. Atualiza a tabela de páginas e a fila LRU

    Retorna o índice do frame onde a página foi carregada
    """
    if frames_livres:
        frame = frames_livres.pop(0)
        print(f"Frame livre encontrado: Frame {frame}")
    else:
        print(f"Memória principal cheia")
        frame = substituir_pagina_lru()

    # Copia os dados do disco para o frame
    conteudo = gerar_conteudo_pagina(processo_id, numero_pagina)
    memoria_principal[frame] = conteudo

    # Atualiza a tabela de páginas
    tabelas_de_paginas[processo_id][numero_pagina]["frame"]    = frame
    tabelas_de_paginas[processo_id][numero_pagina]["presente"] = True

    # Atualiza a fila LRU (página recém-carregada vai para o final)
    atualizar_fila_lru(processo_id, numero_pagina)

    print(f"Página {numero_pagina} do Processo {processo_id} "
          f"carregada no Frame {frame}")

    return frame


# Tradução de endereço

def traduzir_endereco(processo_id, endereco_virtual):
    """
    Traduz um endereço virtual em endereço físico
      1. Decompõe o endereço virtual em (página, offset)
      2. Consulta a tabela de páginas
      3. Se tiver presente traduz diretamente
      4. Se não tiver carrega a página e depois traduz
    """
    numero_pagina, offset = decompor_endereco_virtual(endereco_virtual)

    print(f"\n{'='*70}")
    print(f"  INSTRUÇÃO #{contadores['total'] + 1}")
    print(f"{'='*70}")
    print(f"  Processo        : {processo_id}")
    print(f"  Endereço Virtual: {endereco_virtual} (0x{endereco_virtual})")
    print(f"  Página Virtual  : {numero_pagina}")
    print(f"  Offset          : {offset}")
    print(f"{'─'*70}")

    # Consulta a tabela de páginas do processo
    tabela = tabelas_de_paginas[processo_id]
    entrada = tabela[numero_pagina]

    if entrada["presente"]:
        frame = entrada["frame"]
        contadores["hits"] += 1

        print(f" Página {numero_pagina} já está no Frame {frame}")

        atualizar_fila_lru(processo_id, numero_pagina)

    else:
        contadores["page_faults"] += 1

        print(f" Página {numero_pagina} não está na RAM")
        print(f" Tratando falta de página...")

        frame = carregar_pagina(processo_id, numero_pagina)

    # Calcula o endereço físico
    endereco_fisico = (frame * TAMANHO_PAGINA) + offset

    # Recupera o conteúdo do frame
    conteudo = memoria_principal[frame]

    print(f"{'─'*70}")
    print(f"  Endereço Físico : {endereco_fisico} (0x{endereco_fisico:05X})")
    print(f"  Frame Físico    : {frame}")
    print(f"  Conteúdo        : {conteudo}")
    print(f"{'─'*70}")
    print(f"  Estatísticas até agora -> Hits: {contadores['hits']} | "
          f"Page Faults: {contadores['page_faults']} | "
          f"Total: {contadores['total'] + 1}")

    contadores["total"] += 1

    # Exibe estado atual da fila LRU e frames
    exibir_estado_lru()

    time.sleep(PAUSA_ENTRE_INSTRUCOES)


# Exibição do estado

def exibir_estado_lru():
    """
    Mostra o estado atual da fila LRU e dos frames ocupados.
    """
    print(f"\n Fila LRU (-> mais recente):")
    if fila_lru:
        itens = [f"P{proc}.Pg{pag}" for proc, pag in fila_lru]
        print(f"     [{' -> '.join(itens)}]")
    else:
        print(f"     [vazia]")

    print(f" Frames da RAM:")
    for i in range(TOTAL_FRAMES):
        status = memoria_principal[i] if memoria_principal[i] else "(livre)"
        print(f"     Frame {i}: {status}")
