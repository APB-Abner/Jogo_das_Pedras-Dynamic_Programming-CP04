# Jogo das Pedras — Dynamic Programming (CP04)

Implementação das soluções pedidas no **Checkpoint 04**: função recursiva pura e função recursiva com memoização (via `lru_cache` e via `dict`). Também incluímos uma versão **DP iterativa** (bottom‑up) e uma função auxiliar para **sugerir a melhor jogada**.

## Como rodar

Requer **Python 3.10+**.

```bash
cd jogo_das_pedras
python pedras.py 4 --mode rec     # recursiva pura
python pedras.py 10000 --mode memo  # memo com lru_cache (rápido)
python pedras.py 25 --mode dp       # DP iterativa
```

Saída típica:

``` simple text
n=25: posição VENCEDORA  |  modo=memo  |  0.10 ms
→ Jogada sugerida: tirar 1 pedra(s).
```

## Funções principais

- `vence_rec(n) -> bool`: recursão pura (exponencial).  
- `@lru_cache vence_memo_lru(n) -> bool`: recursão com memoização (rápido).  
- `vence_memo_dict(n, memo) -> bool`: memoização manual com dicionário.  
- `vence_dp_iter(n) -> bool`: bottom-up (O(n)).  
- `melhor_jogada(n, solver) -> int|None`: retorna 1, 2 ou 3 se houver jogada vencedora.

## Ideia (resumo)

Uma posição é **vencedora** se **existe** um movimento (tirar 1, 2 ou 3) que deixa o oponente em posição **perdedora**.  
Formalmente: `V(n) = any(not V(n-k) for k in {1,2,3} if n-k>=0)` com `V(0)=False`.  
Isso gera o conhecido padrão de que os múltiplos de **4** são perdedores (0,4,8,12,16, ...).

## Complexidade

- Recursiva pura: **exponencial** (piora rapidamente).  
- Recursiva com memo/DP: **O(n)** tempo e **O(n)** memória.

## Testes rápidos

```bash
python - << 'PY'
from pedras import vence_rec, vence_memo_lru, vence_dp_iter
tab = {0:False,1:True,2:True,3:True,4:False,5:True,6:True,7:True,8:False,9:True,10:True,11:True,12:False,13:True,14:True,15:True,16:False}
print(all(vence_memo_lru(n)==tab[n] for n in tab))
print(vence_memo_lru(10_001))  # deve ser True (não múltiplo de 4)
PY
```

## Estrutura do repositório

``` simpletext
jogo_das_pedras/
├─ pedras.py
└─ README.md
```

## Integrantes

- RM558468 — Abner de Paiva Barbosa
- RM555201 — Fernando Luiz Silva Antonio
- RM554812 — Thomas de Almeida Reichmann
