from pathlib import Path
import time 

plans = {
    p.split(":")[0]: q.strip().split(" ")
    for p in Path("in11.txt").read_text().splitlines() 
    for q in p.split(":")[1:]
}

def f(s: str, cache: dict[tuple[str, bool, bool], int], dac: bool, fft: bool) -> int:
    if s == "dac": dac = True
    if s == "fft": fft = True

    if s == "out" and dac and fft: return 1
    elif s == "out": return 0

    if (s, dac, fft) in cache:
        return cache[(s, dac, fft)]

    nxt = plans[s]

    total = 0
    for ns in nxt:
        hops = f(ns, cache, dac, fft)

        total += hops

        cache[(ns, dac, fft)] = hops

    return total

svr = "svr"
cache = {}

print(f(s=svr, cache=cache, dac=False, fft=False))