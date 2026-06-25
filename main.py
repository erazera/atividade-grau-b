import time

from config import (
    TAMANHO_MEMORIA_VIRTUAL,
    TAMANHO_MEMORIA_PRINCIPAL,
    TAMANHO_PAGINA,
    TOTAL_PAGINAS,
    TOTAL_FRAMES,
)
from memoria import memoria_principal, fila_lru, contadores
from mmu import inicializar_processo, traduzir_endereco
from processos import definir_processos, definir_instrucoes


def main():
    """
    Executa o loop principal que percorre todas as instruções pré-definidas
    """
    # Cabeçalho
    print("=" * 50)
    print("  SIMULADOR DE MEMÓRIA VIRTUAL (MMU)")
    print("  Sistemas Operacionais 2")
    print("=" * 50)
    print()

    # Especificações do hardware simulado
    print("--- Hardware Simulado ---")
    print(f"  Memória Virtual  : {TAMANHO_MEMORIA_VIRTUAL} bytes (1 MB)")
    print(f"  Memória Principal: {TAMANHO_MEMORIA_PRINCIPAL} bytes (64 KB)")
    print(f"  Tamanho da Página: {TAMANHO_PAGINA} bytes (8 KB)")
    print(f"  Total de Páginas : {TOTAL_PAGINAS}")
    print(f"  Total de Frames  : {TOTAL_FRAMES}")
    print(f"  Algoritmo        : LRU (Least Recently Used)")
    print()

    # Criação dos processos
    print("Inicializando processos...")
    processos = definir_processos()
    for proc in processos:
        inicializar_processo(proc["id"], proc["tamanho"])
    print()

    # Carregamento das instruções
    instrucoes = definir_instrucoes()
    total_instrucoes = len(instrucoes)
    print(f"Total de instruções a executar: {total_instrucoes}")
    print("Iniciando simulação...\n")

    time.sleep(1)

    # Loop principal
    for processo_id, endereco_virtual in instrucoes:
        traduzir_endereco(processo_id, endereco_virtual)

    # Relatório final
    print("\n")
    print("=" * 50)
    print("  RELATÓRIO FINAL")
    print("=" * 50)
    print(f"  Total de Instruções: {contadores['total']}")
    print(f"  Hits               : {contadores['hits']}")
    print(f"  Page Faults        : {contadores['page_faults']}")

    if contadores['total'] > 0:
        taxa_hit = (contadores['hits'] / contadores['total']) * 100
        taxa_fault = (contadores['page_faults'] / contadores['total']) * 100
        print(f"  Taxa de Hit        : {taxa_hit:.1f}%")
        print(f"  Taxa de Page Fault : {taxa_fault:.1f}%")

    print()
    print("--- Estado Final da Memória ---")
    for i in range(TOTAL_FRAMES):
        conteudo = memoria_principal[i] if memoria_principal[i] else "(livre)"
        print(f"  Frame {i}: {conteudo}")

    print()
    print("--- Fila LRU Final (-> mais recente) ---")
    if fila_lru:
        itens = [f"P{proc}.Pg{pag}" for proc, pag in fila_lru]
        print(f"  [{' -> '.join(itens)}]")

    print()
    print("Simulação concluída!")


if __name__ == "__main__":
    main()
