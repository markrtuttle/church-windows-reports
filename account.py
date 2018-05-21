#!/usr/bin/env python

# pylint: disable=missing-docstring

import re
import json

import number

################################################################

def clean(string):
    return re.sub(r"\s+", ' ', string).strip()

################################################################

def type_parse(string):
    string = clean(string)
    if string == "":
        string = "Vendor"

    # pylint: disable=too-many-boolean-expressions
    # pylint: disable=bad-continuation

    if (string == "Asset" or
        string == "Liability" or
        string == "Vendor" or
        string == "Fund" or
        string == "Income" or
        string == "Expense"):
        return string
    raise ValueError("Invalid account type "+string)

def type_fmt(string):
    if string is None:
        return None
    return type_parse(string)

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
            self.type_ = type_fmt(string)
        return self.type_

    def name(self, string=None):
        if string is not None:
            self.name_ = clean(string)
        return self.name_

    def number(self, string=None):
        if string is not None:
            self.number_ = number.fmt(string)
        return self.number_

    def parent(self, string=None):
        if string is not None:
            self.parent_ = number.fmt(string)
        return self.parent_

    def children(self, string=None):
        if string is not None:
            self.children_.append(number.fmt(string))
        return self.children_

    def income(self, string=None):
        if string is not None:
            self.income_.append(number.fmt(string))
        return self.income_

    def expense(self, string=None):
        if string is not None:
            self.expense_.append(number.fmt(string))
        return self.expense_

    ################################################################

    def is_asset(self):
        return self.type_ == 'Asset'

    def is_fund(self):
        return self.type_ == 'Fund'

    def is_liability(self):
        return self.type_ == 'Liability'

    def is_vendor(self):
        return self.type_ == 'Vendor'

    def is_income(self):
        return self.type_ == 'Income'

    def is_expense(self):
        return self.type_ == 'Expense'

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
        return json.dumps(self.marshall(), indent=2)

    ################################################################
