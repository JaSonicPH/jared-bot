import random
import math

def randomRGB(lo: int, hi: int):
    lo = math.floor(lo)
    hi = math.floor(hi)
    assert(0 <= lo)
    assert(hi <= 255)
    return sum([random.randint(lo, hi) * (256 ** _) for _ in range(3)])