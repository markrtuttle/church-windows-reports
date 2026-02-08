#!/usr/bin/env python3

# pylint: disable=missing-docstring

"""An account number is a string, typically of the form d.ddd.ddd.ddd.

Account numbers can be compared for order and equality using ordinary string comparison.
"""

################################################################


def from_string(string):
    try:
        parts = string.split(".")
        if len(parts) != 4:
            return string.strip()  # not formal accout numbers

        int0 = int(parts[0])
        int1 = int(parts[1])
        int2 = int(parts[2])
        int3 = int(parts[3])

        if not 0 <= int0 <= 5:
            raise ValueError
        if not 0 <= int1 <= 999:
            raise ValueError
        if not 0 <= int2 <= 999:
            raise ValueError
        if not 0 <= int3 <= 999:
            raise ValueError

        return f"{int0}.{int1:0>3}.{int2:0>3}.{int3:0.3}"
    except ValueError:
        raise ValueError("Illegal account number " + string) from None


def to_string(number):
    return number


################################################################
