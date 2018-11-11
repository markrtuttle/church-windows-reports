#!/usr/bin/env python

# pylint: disable=missing-docstring

"""An amount is an integer giving an amount in cents.

   An amount is just an integer that can be added and compared with
   ordinary integer operations.  Functions convert between a string of
   the form dddd.cc (with an optional sign) giving an amount in
   dollars and cents with and an integer giving an amount in cents.
"""

################################################################

def from_string_fast(string):
    # String is of the form dddd.cc
    if not string[-3:].startswith('.'):
        raise ValueError
    string = string.replace(',', '')
    string = string.replace('.', '')
    return int(string)

def from_string_slow(string):
    """Convert dollars (a string) to cents (an integer)"""

    if not string:
        return None

    try:
        # A dollar value from excel may or may not have a decimal
        # point (eg 3 for 3.00), may or may not have a digit for the
        # dollar portion (eg .03 for 0.03), and may or may not have
        # two digits for the cents (eg, 1.2 for 1.20).

        sign = 1
        if string.startswith('-'):
            sign = -1
            string = string[1:]
        elif string.startswith('+'):
            string = string[1:]

        parts = string.split('.')
        size = len(parts)
        if size == 1:
            dollars = parts[0]
            cents = '00'
        elif size == 2:
            dollars = parts[0]
            cents = parts[1]
        else:
            raise ValueError

        size = len(dollars)
        if size == 0:
            dollars = '0'
        dollars = dollars.replace(',', '')

        size = len(cents)
        if size == 0:
            cents = '00'
        elif size == 1:
            cents = cents + '0'
        elif size == 2:
            pass
        else:
            raise ValueError

        return sign * int(dollars + cents)
    except ValueError:
        raise ValueError("Invalid dollar amount: " + string)

def from_string(string):
    return from_string_slow(string)

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
