# from functools import lru_cache
# import sys

# sys.setrecursionlimit(20000)

# @lru_cache(maxsize=None)
# def fib(m: int) -> bool:
#     if m == 0:
#         return False
#     for k in (1, 2, 3):
#         if m - k >= 0 and not fib(m - k):
#             return True
#     return False

# print([fib(n) for n in range(16)])
# print(fib.cache_info())
# print (fib(10000))
# print(fib.cache_info())



# import sys
# sys.setrecursionlimit(5000)  # 2500 é seguro p/ n=10000

# def win(n: int) -> bool:
#     if n < 0:
#         raise ValueError("n >= 0")
#     if n in (0,):  # perdedor
#         return False
#     if n in (1, 2, 3):  # vencedor
#         return True
#     return win(n - 4)

# print([win(i) for i in range(16)])
# print(win(10000))  # False



# from typing import Callable, Union

# Thunk = Callable[[], Union[bool, "Thunk"]]

# def win_thunk(n: int) -> Thunk | bool:
#     if n == 0:
#         return False
#     if n in (1, 2, 3):
#         return True
#     # mantém a definição recursiva… mas devolve função em vez de chamar já
#     return lambda: win_thunk(n - 4)

# def trampoline(t: Union[bool, Thunk]) -> bool:
#     while callable(t):
#         t = t()
#     return t

# print([trampoline(win_thunk(i)) for i in range(16)])
# print(trampoline(win_thunk(10000)))  # False


def win_mod(n: int) -> bool:
    if n < 4:
        return n != 0
    # uma única chamada recursiva para o resto
    return win_mod(n % 4)

print([win_mod(i) for i in range(16)])
print(win_mod(10000))  # False
