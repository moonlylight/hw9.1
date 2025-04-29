from math import gcd

class Rational:
    def __init__(self, numerator, denominator=None):
        if denominator is None:
            parts = numerator.split('/')
            numerator, denominator = int(parts[0]), int(parts[1])
        self.n = numerator
        self.d = denominator
        self.reduce()

    def reduce(self):
        common_divisor = gcd(self.n, self.d)
        self.n //= common_divisor
        self.d //= common_divisor

    def __add__(self, other):
        if isinstance(other, Rational):
            numerator = self.n * other.d + other.n * self.d
            denominator = self.d * other.d
            return Rational(numerator, denominator)
        elif isinstance(other, int):
            numerator = self.n + other * self.d
            return Rational(numerator, self.d)
        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Rational):
            numerator = self.n * other.d - other.n * self.d
            denominator = self.d * other.d
            return Rational(numerator, denominator)
        elif isinstance(other, int):
            numerator = self.n - other * self.d
            return Rational(numerator, self.d)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return Rational(other * self.d - self.n, self.d)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Rational):
            numerator = self.n * other.n
            denominator = self.d * other.d
            return Rational(numerator, denominator)
        elif isinstance(other, int):
            numerator = self.n * other
            return Rational(numerator, self.d)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Rational):
            numerator = self.n * other.d
            denominator = self.d * other.n
            return Rational(numerator, denominator)
        elif isinstance(other, int):
            numerator = self.n
            denominator = self.d * other
            return Rational(numerator, denominator)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, int):
            numerator = other * self.d
            return Rational(numerator, self.n)
        return NotImplemented

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == "n":
            return self.n
        elif key == "d":
            return self.d

    def __setitem__(self, key, value):
        if key == "n":
            self.n = value
        elif key == "d":
            self.d = value
        self.reduce()


def parse_expression(expr):
    tokens = expr.split()
    if not tokens:  # Порожній рядок
        raise ValueError("Blank line detected")
    parsed_tokens = []
    for token in tokens:
        if '/' in token:
            parts = token.split('/')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                parsed_tokens.append(f"Rational({parts[0]}, {parts[1]})")
            else:
                raise ValueError(f"Invalid fraction format: {token}")
        else:
            parsed_tokens.append(token)
    return ' '.join(parsed_tokens)


def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_number, line in enumerate(infile, start=1):
            try:
                parsed_line = parse_expression(line.strip())
                result = eval(parsed_line, {"Rational": Rational})
                outfile.write(f"{result()}\n")
            except ZeroDivisionError:
                outfile.write(f"Line {line_number}: Error (Division by zero)\n")
            except ValueError as ve:
                outfile.write(f"Line {line_number}: Error ({ve})\n")
            except Exception as e:
                outfile.write(f"Line {line_number}: Error ({e})\n")


process_file("input01.txt", "output.txt")
