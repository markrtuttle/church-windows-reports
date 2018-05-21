#!/usr/bin/env python
# pylint: disable=missing-docstring

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

class IncomeLine(object):
    def __init__(self, line=None):
        self.number_ = None
        self.name_ = None
        self.month_ = None
        self.prior_year_ = None
        self.year_ = None
        self.budget_ = None
        if line is not None:
            self.load(line)

    def load(self, line):
        self.number_ = number.fmt(line[0])
        self.name_ = clean(line[1])
        self.month_ = amount.fmt(line[2])
        self.prior_year_ = amount.fmt(line[3])
        self.year_ = amount.fmt(line[4])
        self.budget_ = amount.fmt(line[6])

    def number(self):
        return self.number_

    def name(self):
        return self.name_

    def month(self):
        return self.month_

    def prior_year(self):
        return self.prior_year_

    def year(self):
        return self.year_

    def budget(self):
        return self.budget_

    def marshall(self):
        return {
            "number": self.number_,
            "name": self.name_,
            "month": self.month_,
            "prior_year": self.prior_year_,
            "year": self.year_,
            "budget": self.budget_
            }

################################################################
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
                if number.is_number(line[0]):
                    detail = IncomeLine(line)
                    self.account_[detail.number()] = detail

    def account(self, nmbr):
        return self.account_[nmbr]

    def accounts(self, nmbrs):
        return [self.account(nmbr) for nmbr in nmbrs]

    def marshall(self):
        my_account = {}
        for nmbr in self.account_:
            my_account[nmbr] = self.account(nmbr).marshall()
        return my_account

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2, sort_keys=True)

################################################################
################################################################

def main():
    inc = Income("old/report/income.csv")
    print inc.dump_jsons()

if __name__ == "__main__":
    main()
