#!/usr/bin/env python

# pylint: disable=missing-docstring

# Unlike other data dumped from Church Windows, we assume a fixed layout
# to the chart of accounts since Church Windows gives no option to change
# the layout of the chart of accounts.

import json

import numbert
import accountt

################################################################

class Chart(object):
    # pylint: disable=too-many-public-methods

    def __init__(self, chart=None):
        # map account name to account number
        self.number_ = {}
        # map account number to account
        self.account_ = {}
        # list of vendors
        self.vendor_ = []

        if chart is not None:
            self.unmarshall(chart)

    ################################################################

    def marshall(self):
        account_dict = {}
        for num in self.account_:
            account_dict[num] = self.account_[num].marshall()

        my_dict = {
            "account": account_dict,
            "vendor": self.vendor_
            }
        return my_dict

    def unmarshall(self, jsn):
        try:
            with open(jsn) as handle:
                my_dict = json.load(handle)

                account = my_dict["account"]
                vendor = my_dict["vendor"]

                for num in account:
                    self.account_[num] = accountt.Account().unmarshall(account[num])
                    self.vendor_ = vendor
                for num in self.account_:
                    act = self.account_[num]
                    self.number_[act.name()] = act.number()
        except:
            raise ValueError("Unable to open chart: " + jsn)

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2, sort_keys=True)

    ################################################################

    def number(self, name, num=None):
        if num is not None:
            self.number_[name] = numbert.from_string(num)
        try:
            return self.number_[name]
        except KeyError:
            if name in self.vendor_:
                return None
            raise

    def account(self, nmbr, act=None, parent=None):
        if act is not None:
            if act.is_vendor():
                self.vendor_.append(act.name())
                return None

            if act.number() != nmbr:
                raise ValueError("Account number mismatch: "+nmbr)

            if parent is not None:
                parent = numbert.from_string(parent)

                if act.parent() is not None and act.parent() != parent:
                    raise ValueError("Parent already defined for " + nmbr)

                act.parent(parent)
                if act.is_income():
                    self.account_[parent].income(nmbr)
                elif act.is_expense():
                    self.account_[parent].expense(nmbr)
                else:
                    self.account_[parent].children(nmbr)

            self.account_[nmbr] = act
            self.number(act.name(), nmbr)

        if nmbr is None:
            return None
        return self.account_[nmbr]

    def assets(self, all_assets=False):
        asset = {}
        for num in self.account_:
            act = self.account_[num]
            if act.is_asset() and (act.parent() is None or all_assets):
                asset[num] = act
        return asset

    def funds(self, all_funds=False):
        fund = {}
        for num in self.account_:
            act = self.account_[num]
            if act.is_fund() and (act.parent() is None or all_funds):
                fund[num] = act
        return fund

    def liabilities(self, all_liabilities=False):
        liability = {}
        for num in self.account_:
            act = self.account_[num]
            if act.is_liability() and (act.parent() is None or all_liabilities):
                liability[num] = act
        return liability

    def vendors(self):
        return self.vendor_

    def income(self, nmbr=None):
        income = {}
        numbers = self.account_
        if nmbr is not None:
            nmbr = numbert.from_string(nmbr)
            numbers = self.account_[nmbr].income()
        for num in numbers:
            income[num] = self.account_[num]
        return income

    def expense(self, nmbr=None):
        expense = {}
        numbers = self.account_
        if nmbr is not None:
            nmbr = numbert.from_string(nmbr)
            numbers = self.account_[nmbr].expense()
        for num in numbers:
            expense[num] = self.account_[num]
        return expense

    def is_account(self, nmbr):
        try:
            return self.account_[nmbr] is not None
        except KeyError:
            return False

    ################################################################

    def validate(self):
        for num in self.account_:
            if self.is_valid_account(num):
                continue
            act = self.account_[num]
            print act.dump_jsons()
            if act.parent() is not None:
                print self.account_[act.parent()].dump_jsons()
            raise ValueError("Found invalid account " + act.number())
        return True

    def is_valid_account(self, num):
        return (self.is_valid_asset(num) or
                self.is_valid_liability(num) or
                self.is_valid_fund(num) or
                self.is_valid_income(num) or
                self.is_valid_expense(num))

    def is_valid_asset(self, num):
        act = self.account_[num]
        valid = True
        valid &= num == act.number()
        valid &= act.is_asset()
        if act.parent() is not None:
            parent = self.account_[act.parent()]
            valid &= parent.is_asset()
            valid &= self.is_parent_child(parent.number(), act.number())
        for num_ in act.children():
            child_ = self.account_[num_]
            valid &= child_.is_asset()
            valid &= self.is_parent_child(act.number(), child_.number())
        valid &= len(act.income()) == 0 and len(act.expense()) == 0
        return valid

    def is_valid_liability(self, num):
        act = self.account_[num]
        valid = True
        valid &= num == act.number()
        valid &= act.is_liability()
        if act.parent() is not None:
            parent = self.account_[act.parent()]
            valid &= parent.is_liability()
            valid &= self.is_parent_child(parent.number(), act.number())
        for num_ in act.children():
            child_ = self.account_[num_]
            valid &= child_.is_liability()
            valid &= self.is_parent_child(act.number(), child_.number())
        valid &= len(act.income()) == 0 and len(act.expense()) == 0
        return valid

    def is_valid_fund(self, num):
        act = self.account_[num]
        valid = True
        valid &= num == act.number()
        valid &= act.is_fund()
        if act.parent() is not None:
            parent = self.account_[act.parent()]
            valid &= parent.is_fund()
            valid &= self.is_parent_child(parent.number(), act.number())
        for num_ in act.children():
            child_ = self.account_[num_]
            valid &= child_.is_fund()
            valid &= self.is_parent_child(act.number(), child_.number())
        for num_ in act.income():
            child_ = self.account_[num_]
            valid &= child_.is_income()
            valid &= self.is_parent_child_income(act.number(), child_.number())
        for num_ in act.expense():
            child_ = self.account_[num_]
            valid &= child_.is_expense()
            valid &= self.is_parent_child_expense(act.number(), child_.number())
        valid &= (len(act.children()) == 0 or
                  len(act.income()) == 0 and len(act.expense()) == 0)
        return valid

    def is_valid_income(self, num):
        act = self.account_[num]
        valid = True
        valid &= num == act.number()
        valid &= act.is_income()
        if act.parent() is not None:
            parent = self.account_[act.parent()]
            valid &= parent.is_fund()
            valid &= self.is_parent_child_income(parent.number(), act.number())
        valid &= len(act.children()) == 0
        valid &= len(act.income()) == 0 and len(act.expense()) == 0
        return valid

    def is_valid_expense(self, num):
        act = self.account_[num]
        valid = True
        valid &= num == act.number()
        valid &= act.is_expense()
        if act.parent() is not None:
            parent = self.account_[act.parent()]
            valid &= parent.is_fund()
            valid &= self.is_parent_child_expense(parent.number(), act.number())
        valid &= len(act.children()) == 0
        valid &= len(act.income()) == 0 and len(act.expense()) == 0
        return valid

    ################################################################

    def is_parent_child(self, num1, num2):
        parent = self.account_[num1]
        child = self.account_[num2]
        return (child.parent() == parent.number()
                and
                child.number() in parent.children())

    def is_parent_child_income(self, num1, num2):
        parent = self.account_[num1]
        child = self.account_[num2]
        return (child.parent() == parent.number()
                and
                child.number() in parent.income())

    def is_parent_child_expense(self, num1, num2):
        parent = self.account_[num1]
        child = self.account_[num2]
        return (child.parent() == parent.number()
                and
                child.number() in parent.expense())

################################################################
