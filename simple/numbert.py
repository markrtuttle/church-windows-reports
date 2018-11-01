#!/usr/bin/env python

# pylint: disable=missing-docstring

"""An account number is a string, typically of the form d.ddd.ddd.ddd.

   Account numbers can be compared for order and equality using ordinary string comparison.
"""

################################################################

def from_string(string):
    try:
        parts = string.split('.')
        if len(parts) != 4:
            return string.strip() # not formal accout numbers

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

        return "{}.{:0>3}.{:0>3}.{:0.3}".format(int0, int1, int2, int3)
    except ValueError:
        raise ValueError("Illegal account number " + string)

def to_string(number):
    return number

################################################################
