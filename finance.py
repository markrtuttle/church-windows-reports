#!/usr/bin/env python

# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

# TODO: unassigned fund details missing income/expense accounts for funds

import statement

################################################################

class Finance(object):
    # pylint: disable=too-many-public-methods

    def __init__(self, coa_, balance_, income_, journal_, ministry_, args=None):
        self.coa_ = coa_
        self.balance_ = balance_
        self.income_ = income_
        self.journal_ = journal_
        self.ministry_ = ministry_
        self.month = None
        self.year = None
        self.date_start = None
        self.date_end = None
        self.posted_start = None
        self.entries = None

        if args is None:
            return

        self.month = args.month_name
        self.year = args.year
        self.date_start = args.date_start
        self.date_end = args.date_end
        self.posted_start = args.posted_start
        self.line_width = args.line_width
        self.entries = journal_.period_entries(args.date_start,
                                               args.date_end,
                                               args.posted_start)

    ################################################################

    def ministry_general_fund_summary(self, ministry_name):
        numbers = self.ministry_.accounts(ministry_name)
        statement.income_statement(numbers, self.income_,
                                   "Budget summary",
                                   self.month, self.year)

    def ministry_general_fund_details(self, ministry_name):
        numbers = self.ministry_.accounts(ministry_name)
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    "Budget details", self.entries)

    def ministry_fund_summary(self, ministry_name):
        numbers = self.ministry_.funds(ministry_name)
        statement.balance_statement(numbers, self.balance_,
                                    "Fund summary", self.month)

    def ministry_fund_details(self, ministry_name):
        numbers = self.ministry_.funds_accounts(ministry_name)
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    "Fund details", self.entries)

    def ministry_report(self, name):
        print ("** {} ministry for {} {} **"
               .format(self.ministry_.name(name), self.month, self.year))

        self.ministry_general_fund_summary(name)
        self.ministry_fund_summary(name)
        self.ministry_general_fund_details(name)
        self.ministry_fund_details(name)

    def ministry_reports(self, newpage=True):
        for fund in self.ministry_.keys():
            self.ministry_report(fund)
            print "\f" if newpage else ""

    ################################################################

    def unassigned_general_fund_summary(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name)
                   for name in unused["income"] + unused["expense"]]
        statement.income_statement(numbers, self.income_,
                                   "Budget summary",
                                   self.month, self.year)

    def unassigned_general_fund_details(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name)
                   for name in unused["income"] + unused["expense"]]
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    "Budget details", self.entries)

    def unassigned_fund_summary(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name) for name in unused["fund"]]
        statement.balance_statement(numbers, self.balance_,
                                    "Fund summary", self.month)

    def unassigned_fund_details(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name) for name in unused["fund"]]
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    "Fund details", self.entries)

    def unassigned_asset_summary(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name) for name in unused["asset"]]
        statement.balance_statement(numbers, self.balance_,
                                    "Asset summary", self.month)

    def unassigned_asset_details(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name) for name in unused["asset"]
                   if name != "Cambridge Savings Bank Checking"]
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    "Asset details", self.entries)

    def unassigned_liability_summary(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name) for name in unused["liability"]]
        statement.balance_statement(numbers, self.balance_,
                                    "Liability summary", self.month)

    def unassigned_liability_details(self, name):
        unused = self.ministry_.accounts_[name]
        numbers = [self.coa_.number(name) for name in unused["liability"]]
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    "Liability details", self.entries)


    def unassigned_report(self, name):
        print "\n** Unassigned accounts **"

        print "\nSummary"
        self.unassigned_general_fund_summary(name)
        self.unassigned_asset_summary(name)
        self.unassigned_liability_summary(name)
        self.unassigned_fund_summary(name)
        print "\nDetails"
        self.unassigned_general_fund_details(name)
        self.unassigned_asset_details(name)
        self.unassigned_liability_details(name)
        self.unassigned_fund_details(name)

    def unassigned_reports(self):
        for fund in self.ministry_.keys_unassigned():
            self.unassigned_report(fund)

################################################################
