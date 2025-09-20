# Jogo das Pedras — Recursão e Estratégias (CP04)

Este projeto implementa e compara **várias versões recursivas** para o clássico *Jogo das Pedras* (cada jogada remove `1`, `2` ou `3` pedras; **vence** quem deixa o oponente **sem jogada**).  
O objetivo pedagógico é mostrar **diferentes abordagens recursivas**, seus **trade‑offs** de desempenho e **profundidade de pilha**, incluindo técnicas como **trampolim** e **redução por módulo**.

> **Padrão do jogo:** posições **perdedoras** são exatamente os **múltiplos de 4**.

---

## Requisitos

- Python **3.10+**

---

## Modos implementados (funções)

Arquivo principal: `pedras.py`

| Modo CLI (`--mode`) | Função               | Estilo                         | Complexidade (tempo) | Pilha | Observações |
|---|---|---|---:|---:|---|
| `rec`        | `vence_rec(n)`        | Recursiva pura                  | Exponencial          | ↑↑↑   | Didática; fica muito lenta p/ `n` grande. |
| `memo`       | `vence_memo_lru(n)`   | Recursiva + `lru_cache`         | O(n)                 | ↑     | Pode exigir `setrecursionlimit` p/ `n` muito grande. |
| `dict`       | `vence_memo_dict(n)`  | Recursiva + dicionário          | O(n)                 | ↑     | Alternativa à `lru_cache`. |
| `dp`         | `vence_dp_iter(n)`    | Iterativa (bottom‑up)           | O(n)                 | –     | Não é recursiva; base de comparação. |
| `trampolim`  | `vence_trampolim(n)`  | **Recursiva com trampolim**     | O(n/4)\*             | **Constante** | Retorna *thunks*; laço externo executa. |
| `modulo`     | `vence_mod(n)`        | **Recursiva por módulo (mod 4)**| O(1)                 | O(1)  | Usa periodicidade; 1 chamada recursiva p/ `n % 4`. |
| `verdadeira` | `vence_verdadeira(n)` | **Recursiva “–4”**              | O(n/4)               | ↑     | “Recursão de verdade” reduzindo por 4. |

\* No `trampolim`, o número de *passos* é ~`n/4` (redução por 4), **sem** crescimento da pilha.

Também há a função utilitária:

- `melhor_jogada(n, solver)` → sugere `1`, `2` ou `3` se houver jogada vencedora.

---

## Uso (CLI)

```bash
# recursiva pura (lenta p/ n grande)
python pedras.py 16 --mode rec

# recursiva com memoização (lru_cache)
python pedras.py 10000 --mode memo

# recursiva com dicionário (memo explícita)
python pedras.py 10000 --mode dict

# DP iterativa (referência, não recursiva)
python pedras.py 10000 --mode dp

# recursiva com trampolim (sem crescimento de pilha)
python pedras.py 10000 --mode trampolim

# recursiva via periodicidade (mod 4) — profundidade O(1)
python pedras.py 10000 --mode modulo

# recursão "verdadeira" reduzindo por 4 (profundidade ~ n/4)
python pedras.py 10000 --mode verdadeira
```

Saída típica:

```bash
n=25: posição VENCEDORA  |  modo=memo  |  0.12 ms
→ Jogada sugerida: tirar 1 pedra(s).
```

### Opções

- `--no-suggest` → não exibe a jogada sugerida.

---

## Importando como biblioteca

```python
from pedras import (
    vence_rec, vence_memo_lru, vence_memo_dict,
    vence_dp_iter, vence_trampolim, vence_mod, vence_verdadeira,
    melhor_jogada,
)

n = 25
print(vence_trampolim(n))           # True
print(melhor_jogada(n, vence_mod))  # 1, 2 ou 3
```

---

## Correção conhecida (padrão do jogo)

Para todos os `n >= 0`:

- `vence_mod(n)` é verdadeiro **sse** `n % 4 != 0`.

Teste rápido:

```python
assert all( (n % 4 != 0) == vence_mod(n) for n in range(0, 1000) )
```

---

## Testes rápidos (exemplo)

```python
# 0..15 (sequência esperada: F, V, V, V, F, V, V, V, F, ...)
esperado = [False, True, True, True] * 4
funs = [vence_rec, vence_memo_lru, vence_memo_dict, vence_trampolim, vence_mod, vence_verdadeira]
for f in funs:
    got = [f(i) for i in range(16)]
    assert got == esperado, f"Falhou em {f.__name__}: {got}"
```

---

## Conceitos chave

- **Trampolim (trampoline):** técnica que preserva o estilo recursivo sem crescer a pilha. A função retorna *thunks* (funções sem argumento com o “próximo passo”), e um laço os executa até obter um valor final.
- **Periodicidade (módulo):** neste jogo, a estrutura de ganhos/perdas se repete a cada 4; por isso, podemos saltar diretamente para `n % 4`.
- **Memoização:** evita recomputações em subproblemas; pode ser via `functools.lru_cache` ou dicionário interno.
- **DP iterativa:** alternativa não recursiva que constrói soluções de baixo para cima.
