from itertools import count

contador = count()
for i in range(0, 10):
    print(contador)
    next(contador)