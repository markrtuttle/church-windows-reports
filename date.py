#!/usr/bin/env python

# pylint: disable=missing-docstring

import re

################################################################

def clean(string):
    return re.sub(r"\s+", ' ', string).strip()

################################################################

def parse(string):
    string = clean(string)

    # ignore timestamp in date-timestamp pair
    space = string.find(" ")
    if space >= 0:
        string = string[:space]

    try:
        parts = string.split('/')
        if len(parts) != 3:
            raise ValueError
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])

        # pylint: disable=misplaced-comparison-constant
        if 0 <= year and year <= 99:
            year = year + 2000

        if not (1 <= month and month <= 12):
            raise ValueError
        if not (1 <= day and day <= 31):
            raise ValueError
        if not (1970 <= year and year <= 2070):
            raise ValueError

        return (month, day, year)
    except ValueError:
        raise ValueError("Invalid date "+string)

def fmt(string, include_year=True, pad=True):
    if string is None:
        return None

    (month, day, year) = parse(string)
    if include_year:
        if not pad:
            return "{}/{}/{}".format(month, day, year)
        return "{:0>2}/{:0>2}/{:0>4}".format(month, day, year)
    if not pad:
        return "{}/{}".format(month, day)
    return "{:0>2}/{:0>2}".format(month, day)

################################################################

def key(string):
    (month, day, year) = parse(string)
    return (year * 100 + month) * 100 + day

def compare(date1, date2):
    if date1 is None or date2 is None:
        raise ValueError
    return cmp(key(date1), key(date2))

def lt(date1, date2):
    # pylint: disable=invalid-name
    if date1 is None or date2 is None:
        return False
    return compare(date1, date2) < 0

def le(date1, date2):
    # pylint: disable=invalid-name
    if date1 is None or date2 is None:
        return False
    return compare(date1, date2) <= 0

def eq(date1, date2):
    # pylint: disable=invalid-name
    if date1 is None or date2 is None:
        return False
    return compare(date1, date2) == 0

def ge(date1, date2):
    # pylint: disable=invalid-name
    if date1 is None or date2 is None:
        return False
    return compare(date1, date2) >= 0

def gt(date1, date2):
    # pylint: disable=invalid-name
    if date1 is None or date2 is None:
        return False
    return compare(date1, date2) > 0

################################################################
