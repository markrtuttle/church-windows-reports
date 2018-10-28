#!/usr/bin/env python
# pylint: disable=missing-docstring

import re
import csv
import json

import number
import amount

################################################################

HEADER_MAP = {
    "Account #": "number",
    "Account Name": "name",
    "Period Activity": "month",
    "Monthly Budget": "month_budget",
    "% of Budget Month": "percent_month_budget",
    "YTD Balance": "ytd",
    "Budget YTD": "ytd_budget",
    "% of Budget YTD": "percent_ytd_budget",
    "Over/Under YTD+(-)": "over_under_ytd",
    "Previous YTD": "prior_ytd",
    "Annual Budget ": "budget",
    "Annual Budget Remaining": "remaining_budget",
    "% of Annual Budget": "percent_budget"
}

KEYS = HEADER_MAP.values()

def is_header(string):
    string = clean(string)
    return string == "Account #"

def column_map(headers):
    col_map = {}
    index = 0
    for header in headers:
        if header:
            try:
                key = HEADER_MAP[header]
            except KeyError:
                raise KeyError("Header {} not in header map".format(header))
        else:
            key = None
        col_map[index] = key
        index += 1
    return col_map

################################################################

def clean(string):
    if string is None:
        return None
    string = re.sub(r"\s+", ' ', string)
    return string.strip()

################################################################

class IncomeLine(object):
    def __init__(self, line=None, col_map=None):
        self.element = {}
        if line is not None and col_map is not None:
            self.load(line, col_map)

    def load(self, columns, col_map):
        index = 0
        for col in columns:
            key = col_map[index]
            self.set(key, col)
            index += 1

    def set(self, key, val):
        if key is None:
            return None

        key = clean(key)
        if not key in KEYS:
            raise ValueError("Unknown entry key "+key)

        if val is None:
            return self.element.get(key)

        if key in ["number"]:
            self.element[key] = number.fmt(val)
        elif key in ["month", "month_budget", "ytd", "ytd_budget",
                     "over_under_ytd", "prior_ytd",
                     "budget", "remaining_budget"]:
            self.element[key] = amount.fmt(val)
        else:
            self.element[key] = clean(val)

        return self.element.get(key)

    ################################################################

    def number(self, val=None):
        return self.set("number", val)
    def name(self, val=None):
        return self.set("name", val)
    def month(self, val=None):
        return self.set("month", val)
    def month_budget(self, val=None):
        return self.set("month_budget", val)
    def percent_month_budget(self, val=None):
        return self.set("percent_month_budget", val)
    def ytd(self, val=None):
        return self.set("ytd", val)
    def ytd_budget(self, val=None):
        return self.set("ytd_budget", val)
    def percent_ytd_budget(self, val=None):
        return self.set("percent_ytd_budget", val)
    def over_under_ytd(self, val=None):
        return self.set("over_under_ytd", val)
    def prior_ytd(self, val=None):
        return self.set("prior_ytd", val)
    def budget(self, val=None):
        return self.set("budget", val)
    def remaining_budget(self, val=None):
        return self.set("remaining_budget", val)
    def percent_budget(self, val=None):
        return self.set("percent_budget", val)

    ################################################################

    def marshall(self):
        return self.element

################################################################

class Income(object):
    def __init__(self, income=None):
        self.account_ = {}
        if income is not None:
            self.load(income)

    def load(self, income):
        with open(income, 'r') as handle:
            for line in csv.reader(handle):
                line += ["", "", "", "", "", "", "", ""]
                if is_header(line[0]):
                    col_map = column_map(line)
                    continue
                if number.is_number(line[0]):
                    detail = IncomeLine(line, col_map)
                    self.account_[detail.number()] = detail

    ################################################################

    def account(self, nmbr):
        return self.account_[nmbr]

    def accounts(self, nmbrs):
        return [self.account(nmbr) for nmbr in nmbrs]

    ################################################################

    def marshall(self):
        my_account = {}
        for nmbr in self.account_:
            my_account[nmbr] = self.account(nmbr).marshall()
        return my_account

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2, sort_keys=True)

################################################################
