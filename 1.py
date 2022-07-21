from math import factorial as fa


def chudnovsky(digits):
    x = 0
    for k in range(digits):
        sign = -1 ** k
        x += (
            (sign * fa(6 * k) * (13591409 + 545140134 * k))
            /
            (fa(3 * k) * (fa(k)**3) * ((640320**3)**(k + 0.5)))
        )
    x *= -12
    x = 1 / x
    return x


def external_example():
    from math import factorial as fact

    i = 1
    sgn = -1
    a = 13591409
    b = 545140134
    c = 640320
    d = c ** (3/2)
    s = a / d
    ss = 3
    while str(ss)[:12] != '3.1415926535' :
        tmp = (sgn * fact(6*i) * (a + b*i) /
        (fact(3*i) * fact(i) ** 3 * d * c**(3*i)))
        s += tmp
        sgn *= -1
        i += 1
        ss = 1 / (12*s)
    print(ss)
    print(i-1)


if __name__ == '__main__':
    external_example()
    exit(0)
    for i in range(1, 12):
        print(i, ':', chudnovsky(i))
