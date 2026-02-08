#!/usr/bin/env python3

# pylint: disable=missing-docstring

"""A date is a string of the form yyyy/mm/dd.

Dates yyyy/mm/dd can be compared for order using ordinary string
comparison.  Functions convert between strings giving dates of the
form mm/dd/yyyy and dates of the form yyyy/mm/dd.
"""

import time
import calendar

################################################################


def from_string(string, first_day=True):
    """Parse a date of the form m or m/y or m/d/y with defaults for d and y"""
    if string is None:
        return None
    if not string:
        string = str(this_month())

    # ignore time in timestamp "mm/dd/yyyy hh:mm:ss"
    space = string.find(" ")
    if space >= 0:
        string = string[:space]

    try:
        parts = [int(num) for num in string.split("/")]

        size = len(parts)
        if size < 1 or size > 3:
            raise ValueError

        if size == 1:
            month, day, year = (parts[0], None, None)
        elif size == 2:
            month, day, year = (parts[0], None, parts[1])
        else:
            month, day, year = (parts[0], parts[1], parts[2])

        if year is None:
            year = this_year()

        if day is None:
            if first_day:
                day = 1
            else:
                day = last_day(month, year)

        return make_ymd_string(month, day, year)
    except (ValueError, IndexError):
        raise ValueError("Not a valid date: {}".format(string))


def to_string(date):
    if date is None:
        return ""

    month, day, year = parse_ymd_string(date)
    return make_mdy_string(month, day, year)


################################################################


def validate_mdy(month, day, year):
    # pylint: disable=misplaced-comparison-constant
    if 0 <= year and year <= 99:
        year = year + 2000

    if not (1 <= month and month <= 12):
        raise ValueError("Invalid month: {}".format(month))
    if not (1 <= day and day <= 31):
        raise ValueError("Invalid day: {}".format(day))
    if not (1970 <= year and year <= 2070):
        raise ValueError("Invalid year: {}".format(year))

    return (month, day, year)


def parse_mdy_string(string):
    try:
        month, day, year = string.split("/")
        month, day, year = validate_mdy(int(month), int(day), int(year))
        return (month, day, year)
    except:
        raise ValueError("Invalid date: " + string)


def parse_ymd_string(string):
    try:
        year, month, day = string.split("/")
        month, day, year = validate_mdy(int(month), int(day), int(year))
        return (month, day, year)
    except:
        raise ValueError("Invalid date: " + string)


def make_mdy_string(month, day, year, with_year=True, with_pad=True):
    month, day, year = validate_mdy(month, day, year)

    if with_pad:
        month = "{:0>2}".format(month)
        day = "{:0>2}".format(day)
        year = "{:0>4}".format(year)

    if with_year:
        return "{}/{}/{}".format(month, day, year)

    return "{}/{}".format(month, day)


def make_ymd_string(month, day, year, with_year=True, with_pad=True):
    month, day, year = validate_mdy(month, day, year)

    if with_pad:
        month = "{:0>2}".format(month)
        day = "{:0>2}".format(day)
        year = "{:0>4}".format(year)

    if with_year:
        return "{}/{}/{}".format(year, month, day)

    return "{}/{}".format(month, day)


################################################################


def month_name(month):
    return calendar.month_name[month]


def last_day(month, year):
    _, month_size = calendar.monthrange(year, month)
    return month_size


def this_day():
    return time.localtime().tm_mday


def this_month():
    return time.localtime().tm_mon


def this_year():
    return time.localtime().tm_year


def today():
    date = time.localtime()
    return (date.tm_mon, date.tm_mday, date.tm_year)


def today_string():
    month, day, year = today()
    return make_mdy_string(month, day, year)


################################################################
