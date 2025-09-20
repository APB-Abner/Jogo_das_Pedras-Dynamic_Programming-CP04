"""
Jogo das Pedras (retira 1, 2 ou 3) — 5 variações recursivas

1) Recursiva pura (sem memoização):            vence_pura(n)
2) Recursiva com memoização (lru_cache):       vence_memo_lru(n)
3) Recursão com TRAMPOLIM (thunks + laço):     vence_trampolim(n)
4) Recursão com MÓDULO (periodicidade mod 4):  vence_mod(n)
5) Recursão verdadeira (-4) (profundidade n/4): vence_verdadeira(n)

Notas:
- (1) é exponencial e serve para fins didáticos; evite n grande.
- (2) é O(n) em tempo/memória, mas ainda usa pilha; para n muito grande pode precisar aumentar recursionlimit.
- (3) mantém estilo recursivo, mas NÃO cresce a pilha (usa loop trampolim).
- (4) usa propriedade matemática: múltiplos de 4 são perdedores.
- (5) "Recursão verdadeira (1)" que sugeri: reduz por 4, então profundidade ≈ n/4 (ainda cresce a pilha).
"""

from __future__ import annotations
from functools import lru_cache
from typing import Callable, Union, Tuple
import sys

MOVES: Tuple[int, int, int] = (1, 2, 3)


def _valida_n(n: int) -> None:
    if not isinstance(n, int) or n < 0:
        raise ValueError("n deve ser inteiro >= 0")


# 1) Recursiva pura (sem memoização) — complexidade exponencial
def vence_pura(n: int) -> bool:
    """
    True  -> existe movimento (1,2,3) que leva o oponente a perder
    False -> todos os movimentos levam o oponente a ganhar
    """
    _valida_n(n)
    if n == 0:
        return False  # sem jogada -> perdedor
    for k in MOVES:
        if n - k >= 0 and not vence_pura(n - k):
            return True
    return False


# 2) Recursiva com memoização (lru_cache) — O(n) tempo / O(n) memória
@lru_cache(maxsize=None)
def _vence_cached(n: int) -> bool:
    if n == 0:
        return False
    return any(n - k >= 0 and not _vence_cached(n - k) for k in MOVES)


def vence_memo_lru(n: int) -> bool:
    """
    Usa lru_cache para armazenar subproblemas.
    Ajusta recursionlimit para suportar profundidade ~n (cuidado com a pilha do SO).
    """
    _valida_n(n)
    needed = max(1000, n + 1000)  # folga
    if sys.getrecursionlimit() < needed:
        try:
            sys.setrecursionlimit(needed)
        except Exception:
            pass
    return _vence_cached(n)


# 3) Recursão com TRAMPOLIM (profundidade constante)
Thunk = Callable[[], Union[bool, "Thunk"]]

def _vence_thunk(n: int) -> Union[bool, Thunk]:
    """
    Em vez de chamar recursivamente, retorna um 'thunk' (função sem args)
    que descreve o próximo passo. Um laço externo (trampolim) executa até
    obter bool. Usamos redução -4 para eficiência mantendo estilo recursivo.
    """
    if n == 0:
        return False
    if n in (1, 2, 3):
        return True
    return lambda: _vence_thunk(n - 4)

def _trampoline(t: Union[bool, Thunk]) -> bool:
    while callable(t):
        t = t()
    return t

def vence_trampolim(n: int) -> bool:
    _valida_n(n)
    return _trampoline(_vence_thunk(n))


# 4) Recursão com MÓDULO (usa periodicidade mod 4; profundidade O(1))
def vence_mod(n: int) -> bool:
    """
    Posições perdedoras: n % 4 == 0.
    Mantém uma chamada recursiva para enfatizar "recursão", mas resolve em O(1).
    """
    _valida_n(n)
    if n < 4:
        return n != 0
    return vence_mod(n % 4)


# 5) Recursão verdadeira (-4) — profundidade ~ n/4
def vence_verdadeira(n: int) -> bool:
    """
    Recursão simples reduzindo em 4 até alcançar casos-base.
    Útil para demonstrar recursão "de verdade" com menos profundidade que -1.
    """
    _valida_n(n)
    if n == 0:
        return False
    if n in (1, 2, 3):
        return True
    return vence_verdadeira(n - 4)


# --- CLI / exemplos ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Jogo das Pedras: decide se vence com n pedras (retira 1,2,3).")
    parser.add_argument("n", type=int, help="n >= 0")
    parser.add_argument(
        "--metodo",
        choices=["pura", "memo_lru", "trampolim", "modulo", "verdadeira"],
        default="trampolim"
    )
    args = parser.parse_args()

    if args.metodo == "pura":
        ans = vence_pura(args.n)
    elif args.metodo == "memo_lru":
        ans = vence_memo_lru(args.n)
    elif args.metodo == "trampolim":
        ans = vence_trampolim(args.n)
    elif args.metodo == "modulo":
        ans = vence_mod(args.n)
    else:  # "verdadeira"
        # Para n muito grande, talvez precise de um recursionlimit maior (~n/4)
        need = args.n // 4 + 100
        if sys.getrecursionlimit() < need:
            try:
                sys.setrecursionlimit(need)
            except Exception:
                pass
        ans = vence_verdadeira(args.n)

    print(f"n = {args.n} -> {'Vence' if ans else 'Perde'} (método: {args.metodo})")


