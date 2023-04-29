import random
lst = ['.', '#', '.', '.', '.']
col = random.randint(10, 30)
row = random.randint(10, 30)

coin = 10
mons = 100

matrix = []
print(col, row)

for i in range(row):
    tmp = []
    for j in range(col):
        tmp.append(random.choice(lst))
    matrix.append(tmp)

for i in matrix:
    for j in i:
        print(j, end='')
    print('')