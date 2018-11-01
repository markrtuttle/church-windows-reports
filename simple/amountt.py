#!/usr/bin/env python

# pylint: disable=missing-docstring

"""An amount is an integer giving an amount in cents.

   An amount is just an integer that can be added and compared with
   ordinary integer operations.  Functions convert between a string of
   the form dddd.cc (with an optional sign) giving an amount in
   dollars and cents with and an integer giving an amount in cents.
"""

################################################################

def from_string(string):
    """Convert dollars (a string) to cents (an integer)"""

    if not string:
        return None

    try:
        # String is of the form dddd.cc
        if not string[-3:].startswith('.'):
            raise ValueError

        string = string.replace(',', '')
        string = string.replace('.', '')
        return int(string)
    except ValueError:
        raise ValueError("Invalid dollar amount: " + string)

def to_string(amount):
    """Convert cents (an integer) to dollars (a string)"""

    if amount is None:
        return ""

    sign = '-' if amount < 0 else ''
    amount = -amount if sign else amount

    dollars = amount / 100
    cents = abs(amount) % 100
    return "{}{}.{:02}".format(sign, dollars, cents)

################################################################
