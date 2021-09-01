def test_method(a, b):
    a = a+1
    c = a+b
    if c<20:
        c=c+5+b
        return b+c
    elif c==2:
        return b
    elif c==3:
        c = c+4
    else:
        c=5*c
        return 6
    return c

print(test_method(10, 3))