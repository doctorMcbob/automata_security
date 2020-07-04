from random import randint
tobin = lambda n, b: (('0' * b) + (bin(n))[2:])[-b:]

W, H = 96, 96

def nbrs(pos, grid):
    X, Y = pos
    ret = ""
    for y in range(Y-1, Y+2):
        for x in range(X-1, X+2):
            if (X, Y) == (x, y): continue
            cell = "1" if (x, y) in grid else "0"
            ret = cell + ret
    return ret

def fresh_start(rand=True):
    grid = set()
    for y in range(H):
        for x in range(W):
            if rand:
                if randint(0, 1): grid.add((x, y))
            elif (x, y) == (W // 2, H // 2): grid.add((x, y))
    return grid

def apply_rule(rule, grid):
    rule = tobin(rule, 256)[::-1]
    new = set()
    for y in range(H):
        for x in range(W):
            n = nbrs((x, y), grid)
            n = int(n, 2)
            if rule[n] == "1":
                new.add((x, y))
    return new

def reduce_to_int(grid):
    binary = ""
    for y in range(H):
        for x in range(W):
            binary += "1" if (x, y) in grid else "0"
    return int(binary, 2)

def undo_reduce(n):
    binary = tobin(n, W*H)
    idx = 0
    grid = set()
    for y in range(H):
        for x in range(W):
            if binary[idx] == "1":
                grid.add((x, y))
            idx += 1
    return grid
