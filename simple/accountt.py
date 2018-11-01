#!/usr/bin/env python

# pylint: disable=missing-docstring

import json

import numbert

################################################################

# The vendor account number
VENDOR = "-A/P Vendor-"

ASSET = "Asset"
LIABILITY = "Liability"
VENDOR = "Vendor"
FUND = "Fund"
INCOME = "Income"
EXPENSE = "Expense"

TYPES = [ASSET, LIABILITY, VENDOR, FUND, INCOME, EXPENSE]

################################################################

class Account(object):

    def __init__(self, typ=None, name=None, nmbr=None):
        self.type_ = None
        self.name_ = None
        self.number_ = None
        self.parent_ = None
        self.children_ = []
        self.income_ = []
        self.expense_ = []
        self.type(typ)
        self.name(name)
        self.number(nmbr)

    ################################################################

    def type(self, string=None):
        if string is not None:
            if string not in TYPES:
                raise ValueError("Illegal type: " + string)
            self.type_ = string
            return self
        return self.type_

    def name(self, string=None):
        if string is not None:
            self.name_ = string.strip()
            return self
        return self.name_

    def number(self, string=None):
        if string is not None:
            self.number_ = numbert.from_string(string)
            return self
        return self.number_

    def parent(self, string=None):
        if string is not None:
            self.parent_ = numbert.from_string(string)
            return self
        return self.parent_

    def children(self, string=None):
        if string is not None:
            self.children_.append(numbert.from_string(string))
            return self
        return self.children_

    def income(self, string=None):
        if string is not None:
            self.income_.append(numbert.from_string(string))
        return self.income_

    def expense(self, string=None):
        if string is not None:
            self.expense_.append(numbert.from_string(string))
            return self
        return self.expense_

    ################################################################

    def is_asset(self):
        return self.type_ == ASSET

    def is_fund(self):
        return self.type_ == FUND

    def is_liability(self):
        return self.type_ == LIABILITY

    def is_vendor(self):
        return self.type_ == VENDOR

    def is_income(self):
        return self.type_ == INCOME

    def is_expense(self):
        return self.type_ == EXPENSE

    def is_debit_account(self):
        return self.is_asset() or self.is_expense()

    def is_credit_account(self):
        return (self.is_fund() or self.is_vendor() or self.is_liability() or
                self.is_expense())

    ################################################################

    def marshall(self):
        return {
            "type": self.type_,
            "name": self.name_,
            "number": self.number_,
            "parent": self.parent_,
            "children": self.children_,
            "income": self.income_,
            "expense": self.expense_
            }

    def unmarshall(self, my_dict):
        self.type(my_dict["type"])
        self.name(my_dict["name"])
        self.number(my_dict["number"])
        self.parent(my_dict["parent"])
        for num in my_dict["children"]:
            self.children(num)
        for num in my_dict["income"]:
            self.income(num)
        for num in my_dict["expense"]:
            self.expense(num)
        return self

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2, sort_keys=True)

    ################################################################
