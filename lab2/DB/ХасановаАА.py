def isHappy(a: int) -> bool:
    n = 0
    b = []
    c = []
    while (a != 1):
        i = 0
        b = []
        n+=1
        while (a != 0):
            b.append(a % 10)
            a = a // 10
            i += 1
        for i in range(len(b)):
            b[i] = b[i] ** 2
            a += b[i]
        print("new_sum", a)
        #c.append(a)
        if (n>2 and a == 4):
            return False
    if (a == 1):
        return True
    elif (a != 1):
        return False