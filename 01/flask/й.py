def getevenlist(l):
    s = 0
    for i in range(0, len(l)):
        for j in [ji for ji in range(i, len(l)) if ji != i]:
            s = s + (1 if (i < j and l[i] > l[j]) or (i > j and l[i] < l[j]) else 0)
    return s


nm = [int(x) for x in input().split()]
n = nm[0]
m = nm[1]

L = []
Le = []
for ni in range(0, n):
    L.extend([int(x) for x in input().split()])
    Le.extend([x + 1 for x in range(len(Le), len(Le) + m) if (x + 1) != n * m] if ni % 2 == 0 else [x + 1 for x in reversed(range(len(Le), len(Le) + m)) if (x + 1) != n * m])

if getevenlist(L) != getevenlist(Le):
    print("Не повезло...")
else:
    print("Бинго!")
