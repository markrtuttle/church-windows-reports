#!/usr/bin/env python

import json

################################################################

# The account types
ASSET = "Asset"
LIABILITY = "Liability"
VENDOR = "Vendor"
FUND = "Fund"
INCOME = "Income"
EXPENSE = "Expense"

TYPES = [ASSET, LIABILITY, VENDOR, FUND, INCOME, EXPENSE]

# The account numbers start with 1 through 5
ASSET_PREFIX = '1'
LIABILITY_PREFIX = '2'
FUND_PREFIX = '3'
INCOME_PREFIX = '4'
EXPENSE_PREFIX = '5'

################################################################

class Account(object):

    def __init__(self, account):
        self.type_ = account['type']
        self.name_ = account['name']
        self.number_ = account['number']
        self.parent_ = account['parent']
        self.children_ = account['children']

    ################################################################

    def type(self):
        return self.type_

    def name(self):
        return self.name_

    def number(self):
        return self.number_

    def parent(self):
        return self.parent_

    def children(self):
        return self.children_

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
        return not self.is_debit_account()

    ################################################################

    def amount(self, debit=None, credit=None):
        amount = (debit or 0) - (credit or 0)
        if self.is_credit_account():
            amount = -amount
        return amount

    ################################################################

    def assets(self):
        return [child for child in self.children_
                if child.startswith(ASSET_PREFIX)]

    def liabilities(self):
        return [child for child in self.children_
                if child.startswith(LIABILITY_PREFIX)]

    def funds(self):
        return [child for child in self.children_
                if child.startswith(FUND_PREFIX)]

    def incomes(self):
        return [child for child in self.children_
                if child.startswith(INCOME_PREFIX)]

    def expenses(self):
        return [child for child in self.children_
                if child.startswith(EXPENSE_PREFIX)]

    ################################################################

    def dictionary(self):
        return {'type': self.type_,
                'name': self.name_,
                'number': self.number_,
                'parent': self.parent_,
                'children': self.children_,
               }

    def string(self):
        return json.dumps(self.dictionary())

################################################################
