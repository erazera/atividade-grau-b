# Simulador de Memória Virtual (MMU)

Simulador de uma MMU (Memory Management Unit) feito em Python para a disciplina de Sistemas Operacionais 2.

O programa simula o ciclo completo de tradução de endereços virtuais para físicos, incluindo tratamento de Page Faults e substituição de páginas com o algoritmo LRU.

## Hardware Simulado

| Parâmetro | Valor |
| :--- | :--- |
| Memória Virtual | 1 MB (128 páginas) |
| Memória Principal (RAM) | 64 KB (8 frames) |
| Tamanho da Página/Frame | 8 KB |
| Algoritmo de Substituição | LRU (Least Recently Used) |

Como temos 128 páginas possíveis mas só 8 frames na RAM, nem tudo cabe ao mesmo tempo e é aí que o LRU entra pra decidir quem sai.

## Estrutura do Projeto

```
├── config.py        → Constantes do hardware (tamanho da RAM, páginas, etc.)
├── memoria.py       → Estruturas de dados (RAM, tabela de páginas, fila LRU)
├── mmu.py           → Lógica da MMU (tradução de endereços, page fault, LRU)
├── processos.py     → Definição dos processos e lista de instruções
└── main.py          → Ponto de entrada e relatório final
```

## Escolhas do Projeto

- **Python** — Pela facilidade
- **LRU com lista ordenada** — a fila LRU é uma lista simples. Quem está na posição 0 é a página mais velha e será a próxima a ser expulsa. A cada acesso, a página vai pro final da fila como a mais recentemente acessada.
- **Loop sequencial (single-thread)** 
- **Instruções fixas (sem random)** — a lista de acessos à memória é pré-definida
## Como Executar

Precisa ter Python 3 instalado.

```bash
python3 main.py
```

A simulação vai exibir cada instrução passo a passo no terminal, mostrando:
- Decomposição do endereço virtual (página + offset)
- Se foi Hit ou Page Fault
- Estado da fila LRU e dos frames da RAM
- Relatório final com taxas de hit e page fault
