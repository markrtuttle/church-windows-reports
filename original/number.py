#!/usr/bin/env python

# pylint: disable=missing-docstring

import re

################################################################

def clean(string):
    return re.sub(r'\s+', ' ', string).strip()

################################################################

def parse(string):
    string = clean(string)

    try:
        parts = string.split('.')
        if len(parts) != 4:
            raise ValueError
        int0 = int(parts[0])
        int1 = int(parts[1])
        int2 = int(parts[2])
        int3 = int(parts[3])

        # pylint: disable=misplaced-comparison-constant
        if not (0 <= int0 and int0 <= 5):
            raise ValueError
        if not (0 <= int1 and int1 <= 999):
            raise ValueError
        if not (0 <= int2 and int2 <= 999):
            raise ValueError
        if not (0 <= int3 and int3 <= 999):
            raise ValueError

        return (int0, int1, int2, int3)
    except ValueError:
        raise ValueError("Illegal account number " + string)

def fmt(string):
    if string is None:
        return None
    if string == '':
        return None
    if string == '-A/P Vendor-':
        return None
    (int0, int1, int2, int3) = parse(string)
    return "{}.{:0>3}.{:0>3}.{:0>3}".format(int0, int1, int2, int3)

def is_number(number):
    try:
        parse(number)
    except ValueError:
        return False
    return True

################################################################

def key(string):
    (int0, int1, int2, int3) = parse(string)
    return ((int0 * 1000 + int1) * 1000 + int2) * 1000 + int3

def compare(number1, number2):
    return cmp(key(number1), key(number2))

def lt(number1, number2):
    # pylint: disable=invalid-name
    if number1 is None or number2 is None:
        return False
    return compare(number1, number2) < 0

def le(number1, number2):
    # pylint: disable=invalid-name
    if number1 is None or number2 is None:
        return False
    return compare(number1, number2) <= 0

def eq(number1, number2):
    # pylint: disable=invalid-name
    if number1 is None or number2 is None:
        return False
    return compare(number1, number2) == 0

def ge(number1, number2):
    # pylint: disable=invalid-name
    if number1 is None or number2 is None:
        return False
    return compare(number1, number2) >= 0

def gt(number1, number2):
    # pylint: disable=invalid-name
    if number1 is None or number2 is None:
        return False
    return compare(number1, number2) > 0

################################################################
