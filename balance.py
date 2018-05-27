#!/usr/bin/env python
# pylint: disable=missing-docstring

from pprint import pprint

import re
import csv
import json

import number
import amount

################################################################

# Note: For the sake of easily identifying funds and subfunds,
# we require that the fund number and name be in columns 0 and 2,
# and the subfund number and name be in columns 1 and 3.

HEADER_MAP = {
    "Account #": "number",
    "Account Name": "name",
    "Beginning Balance": "opening",
    "Period Activity": "month",
    "Previous Period Balance": "month_prior",
    "Amount Diff Period": "month_diff",
    "% Diff Period": "month_diff_percent",
    "YTD Balance": "ytd",
    "Previous Year Balance": "ytd_prior",
    "Amount Diff YTD": "ytd_diff",
    "% Diff YTD": "ytd_diff_percent",
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
    if col_map[0] != "number" or col_map[2] != "name":
        raise ValueError("Account number and name must be balance sheet "
                         "columns 1 and 3.")
    return col_map

################################################################

def clean(string):
    if string is None:
        return None
    string = re.sub(r"\s+", ' ', string)
    return string.strip()

################################################################

class BalanceLine(object):

    def __init__(self, line=None, col_map=None, subfund=False):
        self.element = {}
        if line is not None and col_map is not None:
            self.load(line, col_map, subfund)

    def load(self, line, col_map, subfund=False):
        if not subfund:
            self.number(line[0])
            self.name(line[2])
        else:
            self.number(line[1])
            self.name(line[3])
        index = 4
        for col in line[4:]:
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
        elif key in ["opening", "month", "month_prior", "month_diff",
                     "ytd", "ytd_prior", "ytd_diff"]:
            self.element[key] = amount.fmt(val)
        else:
            self.element[key] = clean(val)

        return self.element.get(key)

    ################################################################

    def number(self, val=None):
        return self.set("number", val)
    def name(self, val=None):
        return self.set("name", val)
    def opening(self, val=None):
        return self.set("opening", val)
    def month(self, val=None):
        return self.set("month", val)
    def month_prior(self, val=None):
        return self.set("month_prior", val)
    def month_diff(self, val=None):
        return self.set("month_diff", val)
    def month_diff_percent(self, val=None):
        return self.set("month_diff_percent", val)
    def ytd(self, val=None):
        return self.set("ytd", val)
    def ytd_prior(self, val=None):
        return self.set("ytd_prior", val)
    def ytd_diff(self, val=None):
        return self.set("ytd_diff", val)
    def ytd_diff_percent(self, val=None):
        return self.set("ytd_diff_percent", val)

    ################################################################

    def marshall(self):
        return self.element

################################################################

class Balance(object):

    def __init__(self, balance=None):
        self.account_ = {}
        self.subfunds_ = []
        if balance is not None:
            self.load(balance)

    def load(self, balance):
        with open(balance, 'r') as handle:
            fund_name = None
            fund_number = None
            fund_children = []
            in_subfunds = False
            col_map = {}
            for line in csv.reader(handle):
                line += ["", "", "", "", "", "", "", ""]
                if is_header(line[0]):
                    col_map = column_map(line)
                    continue
                if number.is_number(line[0]):
                    detail = BalanceLine(line, col_map)
                    self.account_[detail.number()] = detail
                    if in_subfunds: # just ended a list of subfunds
                        self.subfunds_.append((fund_name,
                                               fund_number,
                                               fund_children))
                    fund_name = detail.name()
                    fund_number = detail.number()
                    fund_children = []
                    in_subfunds = False
                    continue
                if number.is_number(line[1]):
                    detail = BalanceLine(line, col_map, subfund=True)
                    self.account_[detail.number()] = detail
                    fund_children.append(detail.number())
                    in_subfunds = True
                    continue
            if in_subfunds: # just ended a list of subfunds
                self.subfunds_.append((fund_name,
                                       fund_number,
                                       fund_children))

    ################################################################

    def account(self, nmbr):
        try:
            return self.account_[nmbr]
        except KeyError:
            raise KeyError("Unknown account number "+nmbr)

    def accounts(self, numbers):
        result = []
        for nmbr in numbers:
            try:
                result.append(self.account(nmbr))
            except KeyError:
                continue
        return result

    def subfunds(self):
        return self.subfunds_

    ################################################################

    def marshall(self):
        my_account = {}
        for nmbr in self.account_:
            my_account[nmbr] = self.account(nmbr).marshall()
        return {"account": my_account, "subfunds": self.subfunds_}

    def dump(self):
        pprint(self.marshall())

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2, sort_keys=True)

################################################################
