
class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = f'Num {num} is not in field range 0 to {prime - 1}'
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f'FieldElement_{self.prime}({self.num})'

    def __eq__(self, other):
        if other is None:
            return False
        return self.prime == other.prime and self.num == other.num

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different Fields')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __rmul__(self, coefficient):
        num = (coefficient * self.num) % self.prime
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        # Fermat's Little Theorem: n^(p - 1) % p = 1;   n > 0
        # b^-1 = b^(p - 2)
        # a/b = a * b^-1 = a * b^(p-2)
        num = (self.num * other.num**(self.prime-2)) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent, modulo=None):
        # b^(p-1) = 1
        # b^-e = b^-e * 1 = b^-e * b^p-1 = b^(p-1-e)
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)


class Point:

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        # Point infinity or zero
        if self.x is None and self.y is None:
            return

        # Validating point
        if self.y**2 != self.x**3 + self.a * self.x + self.b:
            raise ValueError(f'({x}, {y}) is not on the curve')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y \
                and self.a == other.a and self.b == other.b

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        elif isinstance(self.x, FieldElement):
           return 'Point({}, {})_{}_{} FieldElement({})'.format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
        return f'Point({self.x}, {self.y})_{self.a}_{self.b}'

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(f'Points {self}, {other} are not on the same curve')

        if self.x is None:
            return other
        if other.x is None:
            return self

        # the line is in vertical
        # x1 == x2 and y1 != y2
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # when x1 != x2
        # s = (y2 - y1)/(x2 - x1)
        # x3 = s^2 - x1 - x2
        # y3 = s(x1 - x3) - y1
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s**2 - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        # when P1 == P2 and y = 0
        # y = 0, so we cannot calculate slope > s = (3x^2 + a) / 2y
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

        # P1 == P2
        # s = (3x^2 + a) / 2y
        # x3 = s^2 - 2x
        # y3 = s(x - x3) - y
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x3 = s**2 - 2 * self.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        raise NotImplementedError

    def __rmul__(self, coefficient):
        current = self
        result = Point(None, None, self.a, self.b)
        while coefficient:
            if coefficient & 1:
                result += current
            current += current
            coefficient >>= 1
        return result


if __name__ == '__main__':
    prime1 = 223
    a1 = FieldElement(0, prime1)
    b1 = FieldElement(7, prime1)
    x1 = FieldElement(15, prime1)
    y1 = FieldElement(86, prime1)
    point = Point(x1, y1, a1, b1)
    print(point)
    print(7 * point)

    product = point
    p = product
    inf = Point(None, None, a1, b1)
    count = 1
    while product != inf:
        product += p
        count += 1

    print(count)
