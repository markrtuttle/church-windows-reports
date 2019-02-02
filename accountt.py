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

################################################################

# The account numbers start with 1 through 5
ASSET_PREFIX = '1'
LIABILITY_PREFIX = '2'
FUND_PREFIX = '3'
INCOME_PREFIX = '4'
EXPENSE_PREFIX = '5'

def is_asset_number(number):
    return number.startswith(ASSET_PREFIX)

def is_liability_number(number):
    return number.startswith(LIABILITY_PREFIX)

def is_fund_number(number):
    return number.startswith(FUND_PREFIX)

def is_income_number(number):
    return number.startswith(INCOME_PREFIX)

def is_expense_number(number):
    return number.startswith(EXPENSE_PREFIX)

def is_vendor_number(number):
    return number[:1] not in [ASSET_PREFIX, LIABILITY_PREFIX, FUND_PREFIX,
                              INCOME_PREFIX, EXPENSE_PREFIX]

def is_debit_number(number):
    return is_asset_number(number) or is_expense_number(number)

def is_credit_number(number):
    return not is_debit_number(number)

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

    def assets(self, chart=None):
        nums = [child for child in self.children_ if is_asset_number(child)]
        if chart:
            name = lambda num: chart.account(num).name()
            nums = sorted(nums, key=name)
        return nums

    def liabilities(self, chart=None):
        nums = [child for child in self.children_ if is_liability_number(child)]
        if chart:
            name = lambda num: chart.account(num).name()
            nums = sorted(nums, key=name)
        return nums

    def funds(self, chart=None):
        nums = [child for child in self.children_ if is_fund_number(child)]
        if chart:
            name = lambda num: chart.account(num).name()
            nums = sorted(nums, key=name)
        return nums

    def incomes(self, chart=None):
        nums = [child for child in self.children_ if is_income_number(child)]
        if chart:
            name = lambda num: chart.account(num).name()
            nums = sorted(nums, key=name)
        return nums

    def expenses(self, chart=None):
        nums = [child for child in self.children_ if is_expense_number(child)]
        if chart:
            name = lambda num: chart.account(num).name()
            nums = sorted(nums, key=name)
        return nums

    def vendors(self, chart=None):
        nums = [child for child in self.children_ if is_vendor_number(child)]
        if chart:
            name = lambda num: chart.account(num).name()
            nums = sorted(nums, key=name)
        return nums

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
