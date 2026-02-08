#!/usr/bin/env python3

# pylint: disable=missing-docstring

# Unlike other data dumped from Church Windows, we assume a fixed layout
# to the chart of accounts since Church Windows gives no option to change
# the layout of the chart of accounts.

import json

from cwr import accountt

################################################################


class Chart:
    # pylint: disable=too-many-public-methods

    def __init__(self, chart=None):
        # map account number to account description
        self.chart_ = {}
        # map account name to account number
        self.number_ = {}
        self.vendor_name_ = None
        self.vendor_number_ = None

        if chart is not None:
            with open(chart, encoding="utf-8") as handle:
                coa = json.load(handle)
            self.chart_ = coa["account"]
            self.number_ = coa["number"]
            self.vendor_name_ = coa["vendor name"]
            self.vendor_number_ = coa["vendor number"]

        for number in self.chart_:
            self.chart_[number] = accountt.Account(self.chart_[number])

    def accounts(self):
        return list(self.chart_.keys())

    def account(self, number):
        return self.chart_[number]

    def number(self, name):
        return self.number_[name]

    def vendor_name(self):
        return self.vendor_name_

    def vendor_number(self):
        return self.vendor_number_

    ################################################################

    def account_dictionary(self):
        dictionary = {}
        for number in self.accounts():
            dictionary[number] = self.account(number).dictionary()
        return dictionary

    def account_string(self):
        return json.dumps(self.account_dictionary(), indent=2, sort_keys=True)

    def number_dictionary(self):
        return self.number_

    def number_string(self):
        return json.dumps(self.number_dictionary(), indent=2, sort_keys=True)

    def dictionary(self):
        dictionary = {
            "account": self.account_dictionary(),
            "number": self.number_dictionary(),
            "vendor name": self.vendor_name_,
            "vendor number": self.vendor_number_,
        }
        return dictionary

    def string(self):
        return json.dumps(self.dictionary(), indent=2, sort_keys=True)


################################################################
