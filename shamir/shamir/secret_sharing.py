import random
import collections
import sys
import os
import pickle


Point = collections.namedtuple("Point", ["x", "y"])


class Polynomial(list):
    def __call__(self, x):
        return sum(
                    coefficient*(x**power)
                    for power, coefficient in enumerate(self)
                  )

    def __repr__(self):
        return "Polynomial({})".format(super(Polynomial, self).__repr__())


class Shamir:
    PRIME = 251  # TODO: Make more general
    def __init__(self, k, secret):
        if secret >= Shamir.PRIME:
            message = "Secret {} >= {} not supported"
            message = message.format(secret, Shamir.PRIME)
            raise ValueError(message)
        self.k = k
        # Need a polynomial of degree k-1
        # For simplicity, coefficients are non-zero modulo Shamir.Prime
        polynomial = Polynomial([secret])
        polynomial.extend(random.randint(1, Shamir.PRIME - 1)
                          for _ in range(k - 1))
        self.polynomial = polynomial
        # Shares already given
        self.used = set()
        self.used.add(0)  # For simplicity (never give 0 as a share...)

    @staticmethod
    def extract_secret(shares):
        xs = [point.x for point in shares]
        ys = [point.y for point in shares]
        k = len(shares)
        secret = 0
        for j in range(k):
            numerator = ys[j]
            denominator = 1
            for l in range(k):
                if l != j:
                    numerator = (numerator*xs[l])%Shamir.PRIME
                    denominator = (denominator*(xs[l] - xs[j]))%Shamir.PRIME
            secret += Shamir._modular_division(numerator, denominator, Shamir.PRIME)
        secret %= Shamir.PRIME
        return secret

    @staticmethod
    def _modular_division(a, b, n):
        """Division modulo n.

        Adapted from Wikipedia pseudo-code.

        Only returns number relevant to the secret sharing process
        """
        s = 0
        s_prev = 1
        t = 1
        t_prev = 0
        r = b
        r_prev = n
        while r != 0:
            quotient = r_prev//r
            r_prev, r = r, r_prev - quotient*r
            s_prev, s = s, s_prev - quotient*s
            t_prev, t = t, t_prev - quotient*t
        return a*t_prev

    def get_share(self):
        """A share is a point on the curve."""
        if len(self.used) == self.PRIME:
            raise RuntimeError("Out of shares")
        else:
            x = 0
            while x in self.used:
                # TODO: Can run forever... but whatever!
                x = random.randint(1, Shamir.PRIME - 1)
            self.used.add(x)
            return Point(x, self.polynomial(x)%Shamir.PRIME)


if __name__ == "__main__":
    args = sys.argv
    command = args[1]
    if command == "create":
        minimum_required = int(args[2])
        keys_wanted = int(args[3])
        file_name = args[4]
        message = args[5]
        assert not os.path.exists(file_name)
        with open(file_name, "w") as share_file:
            for character in message:
                secret = ord(character)
                shamir = Shamir(minimum_required, secret)
                for _ in range(keys_wanted):
                    share_file.write(repr(shamir.get_share()))
                share_file.write("\n")
    elif command == "extract":
        pass
    else:
        print("Unrecognized command")
