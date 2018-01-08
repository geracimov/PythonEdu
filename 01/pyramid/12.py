def geteve_do_nl_do_ist(l):
    s = 0
    for i in range(0, len(l)):
        for j in [ji for ji in range(i, len(l)) if ji != i]:
            s = s + (1 if (i < j and l[i] > l[j]) or (i > j and l[i] < l[j]) else 0)
    return s


L = [int(x) for x in input().split()]

n = L[0]
l = []
for i in range(0, n):
    l.extend([int(x) for x in input().split()])
print(l)
# w=[1, 2, 3, 4, 8, 7, 6, 5, 9, 10, 11, 12, 15, 14, 13]
# print(w)
print("Бинго!" if getevenlist(l) % 2 == 0 else "Не повезло...")
# print(getEvenList(l))
