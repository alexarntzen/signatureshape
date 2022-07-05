import esig.tosig as ts
from ast import literal_eval as le
from signature import get_words


def test_keys(skeys, pkeys):
    for i in range(len(pkeys)):
        if len(skeys[i + 1]) == 2:
            a = []
        elif len(skeys[i + 1]) == 3:
            a = [le(skeys[i + 1]) - 1]
        else:
            a = [x - 1 for x in list(le(skeys[i + 1]))]

        if not a == pkeys[i]:
            print(a, pkeys[i])


for i in range(2, 20):
    for j in range(2, 20):
        n, d = i, j
        skeys = list(ts.sigkeys(n, d).split(" "))
        if skeys == [""]:
            continue
        pkeys = get_words(n, d)[0]
        test_keys(skeys, pkeys)
