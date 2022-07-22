
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


def get_pi(accuracy: int) -> float:
    if accuracy < 1 or accuracy > 11:
        return 0
    pre_pi = chudnovsky(10)
    pre_pi = str(pre_pi)[:accuracy+2]
    return float(pre_pi)

if __name__ == '__main__':
    print(get_pi(10))
