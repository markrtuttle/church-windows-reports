#!/usr/bin/env python
# pylint: disable=missing-docstring

from pprint import pprint

import re
import csv
import json

import number
import amount

################################################################

def clean(string):
    if string is None:
        return None
    string = re.sub(r"\s+", ' ', string)
    return string.strip()

################################################################
################################################################

class BalanceLine(object):

    def __init__(self, line=None, subfund=False):
        self.number_ = None
        self.name_ = None
        self.month_ = None
        self.year_ = None
        if line is not None:
            self.load(line, subfund)

    def load(self, line, subfund=False):
        if not subfund:
            self.number(line[0])
            self.name(line[2])
        else:
            self.number(line[1])
            self.name(line[3])
        self.month(line[4])
        self.year(line[6])

    ################################################################

    def number(self, string=None):
        if string is not None:
            self.number_ = number.fmt(string)
        return self.number_

    def name(self, string=None):
        if string is not None:
            self.name_ = clean(string)
        return self.name_

    def month(self, string=None):
        if string is not None:
            self.month_ = amount.fmt(string)
        return self.month_

    def year(self, string=None):
        if string is not None:
            self.year_ = amount.fmt(string)
        return self.year_

    ################################################################

    def marshall(self):
        return {
            "number": self.number_,
            "name": self.name_,
            "month": self.month_,
            "year": self.year_,
            }

################################################################
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
            for line in csv.reader(handle):
                line += ["", "", "", "", "", "", "", ""]
                if number.is_number(line[0]):
                    detail = BalanceLine(line)
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
                    detail = BalanceLine(line, subfund=True)
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

def main():
    inc = Balance("old/report/balance.csv")
    print inc.dump_jsons()

if __name__ == "__main__":
    main()

################################################################
