#!/usr/bin/env python

# pylint: disable=missing-docstring

import re

################################################################

def clean(string):
    return re.sub(r"\s+", ' ', string).strip()

################################################################

def parse(amount):
    amount = clean(amount)

    try:
        positive = True
        string = amount

        match = re.match(r'-(.*)', string)
        if match is not None:
            positive = False
            string = match.group(1)

        match = re.match(r'\((.*)\)', string)
        if match is not None:
            positive = False
            string = match.group(1)

        if string.startswith('.'):
            string = "0" + string
        if string.find('.') < 0:
            string = string + ".00"

        parts = string.split('.')
        if len(parts) != 2:
            raise ValueError

        dollars = parts[0]
        dollars = dollars.translate(None, ',')
        dollars = int(dollars)

        cents = parts[1]
        cents = (cents + "00")[:2] if len(cents) < 2 else cents
        cents = int(cents)

        # pylint: disable=misplaced-comparison-constant
        if not (0 <= cents and cents <= 99):
            raise ValueError

        return (positive, dollars, cents)

    except (ValueError, IndexError):
        raise ValueError("Invalid dollar amount "+amount)

def fmt(string, is_debit_account=None, is_debit_entry=None, postfix=False):
    if string is None:
        return None
    if string == "":
        return None
    if string == "N/A":
        return None

    (positive, dollars, cents) = parse(string)
    flip_sign = ((is_debit_account != is_debit_entry and
                  is_debit_account is not None and
                  is_debit_entry is not None)
                 or
                 (not is_debit_entry and
                  is_debit_account is None and
                  is_debit_entry is not None))
    positive = not positive if flip_sign else positive

    if postfix:
        return "{}.{:0>2}{}".format(dollars, cents, " " if positive else "-")
    return "{}{}.{:0>2}".format("" if positive else "-", dollars, cents)


################################################################

def key(amount):
    (positive, dollars, cents) = parse(amount)
    sign = 1 if positive else -1
    return sign * (dollars * 100 + cents)

def compare(amount1, amount2):
    if amount1 is None or amount2 is None:
        raise ValueError
    return cmp(key(amount1), key(amount2))

def lt(amount1, amount2):
    # pylint: disable=invalid-name
    if amount1 is None or amount2 is None:
        return False
    return compare(amount1, amount2) < 0

def le(amount1, amount2):
    # pylint: disable=invalid-name
    if amount1 is None or amount2 is None:
        return False
    return compare(amount1, amount2) <= 0

def eq(amount1, amount2):
    # pylint: disable=invalid-name
    if amount1 is None or amount2 is None:
        return False
    return compare(amount1, amount2) == 0

def ge(amount1, amount2):
    # pylint: disable=invalid-name
    if amount1 is None or amount2 is None:
        return False
    return compare(amount1, amount2) >= 0

def gt(amount1, amount2):
    # pylint: disable=invalid-name
    if amount1 is None or amount2 is None:
        return False
    return compare(amount1, amount2) > 0

################################################################
