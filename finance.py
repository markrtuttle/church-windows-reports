#!/usr/bin/env python

# pylint: disable=missing-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

import date
import amount
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
        self.material_entries = None

        if args is None:
            return

        self.month = args.month_name
        self.year = args.year
        self.date_start = args.date_start
        self.date_end = args.date_end
        self.posted_start = args.posted_start
        self.line_width = args.line_width
        self.compact = args.compact
        self.zeros = args.zeros
        self.entries = reportable_entries(journal_.entries(),
                                          args.date_start,
                                          args.date_end,
                                          args.posted_start)
        self.material_entries = material_entries(self.entries)

    ################################################################

    def ministry_general_fund_summary(self, ministry_name):
        numbers = self.ministry_.accounts(ministry_name)
        return statement.income_statement(numbers, self.income_,
                                          None,
                                          self.month, self.year,
                                          zeros=self.zeros)

    def ministry_general_fund_details(self, ministry_name):
        numbers = self.ministry_.accounts(ministry_name)
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    None, self.entries,
                                    compress=self.compact,
                                    is_debit_account=True)

    def ministry_fund_summary(self, ministry_name):
        numbers = self.ministry_.funds(ministry_name)
        return statement.balance_statement(numbers, self.balance_,
                                           None, self.month,
                                           zeros=self.zeros)

    def ministry_fund_details(self, ministry_name):
        numbers = self.ministry_.funds_accounts(ministry_name)
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    None, self.entries,
                                    compress=self.compact,
                                    is_debit_account=False)

    def ministry_report(self, name, deacons=None):
        print ("** {} ministry for {} {} **"
               .format(self.ministry_.name(name), self.month, self.year))
        if deacons:
            print ", ".join(deacons)

        print "\nGeneral fund"
        if self.ministry_general_fund_summary(name):
            self.ministry_general_fund_details(name)

        print "\nOther funds"
        if self.ministry_fund_summary(name):
            self.ministry_fund_details(name)

        statement.trailer(self.date_start, self.date_end, self.posted_start)

    def ministry_reports(self, newpage=True):
        reports = self.ministry_.keys()
        first_report = True
        for report in reports:
            if not first_report and newpage:
                print "\f"
            first_report = False
            deacons = self.ministry_.accounts_[report].get("deacons")
            self.ministry_report(report, deacons=deacons)

    ################################################################

    def unassigned_general_fund_summary(self):
        numbers = self.ministry_.unassigned_accounts("budget")

        income = [num for num in numbers
                  if self.coa_.account(num).is_income()]
        expense = [num for num in numbers
                   if self.coa_.account(num).is_expense()]

        statement.income_statement(income, self.income_,
                                   None,
                                   self.month, self.year,
                                   zeros=self.zeros,
                                   is_income=True)
        statement.income_statement(expense, self.income_,
                                   None,
                                   self.month, self.year,
                                   zeros=self.zeros,
                                   is_income=False)

    def unassigned_general_fund_details(self):
        numbers = self.ministry_.unassigned_accounts("budget")
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    None, self.entries,
                                    compress=self.compact,
                                    is_debit_account=False)
        # TODO: say why

    def unassigned_fund_summary(self):
        numbers = self.ministry_.unassigned_accounts("fund")
        statement.balance_statement(numbers, self.balance_,
                                    None, self.month,
                                    zeros=self.zeros)

    def unassigned_fund_details(self):
        numbers = self.ministry_.unassigned_funds_accounts()
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    None, self.entries,
                                    compress=self.compact,
                                    is_debit_account=False)

    def unassigned_asset_summary(self):
        numbers = self.ministry_.unassigned_accounts("asset")
        statement.balance_statement(numbers, self.balance_,
                                    None, self.month,
                                    zeros=self.zeros)

    def unassigned_asset_details(self):
        numbers = self.ministry_.unassigned_accounts("asset")
        csb = self.coa_.number("Cambridge Savings Bank Checking")
        numbers = [num for num in numbers if num != csb]
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    None, self.entries,
                                    is_debit_account=True)

    def unassigned_liability_summary(self):
        numbers = self.ministry_.unassigned_accounts("liability")
        statement.balance_statement(numbers, self.balance_,
                                    None, self.month)

    def unassigned_liability_details(self):
        numbers = self.ministry_.unassigned_accounts("liability")
        statement.journal_statement(numbers, self.journal_, self.line_width,
                                    None, self.entries,
                                    is_debit_account=False)

    def unassigned_report(self):
        print "\n** Unassigned accounts **"

        print "\nGeneral fund"
        self.unassigned_general_fund_summary()
        self.unassigned_general_fund_details()

        print "\nAssets"
        self.unassigned_asset_summary()
        self.unassigned_asset_details()

        print "\nLiabilities"
        self.unassigned_liability_summary()
        self.unassigned_liability_details()

        print "\nFunds"
        self.unassigned_fund_summary()
        self.unassigned_fund_details()

        statement.trailer(self.date_start, self.date_end, self.posted_start)

        ################################################################

    def material_report(self):
        ntries = [ntry for ntry in self.journal_.entries() if
                  ntry.is_bill() and
                  amount.ge(ntry.debit(), "100") and
                  (date.ge(ntry.date(), self.date_start) or
                   date.ge(ntry.posted(), self.posted_start))]
        statement.journal_statement(None, self.journal_, self.line_width,
                                    "Significant bills", ntries,
                                    compress=self.compact,
                                    is_debit_account=True,
                                    amount_sort=True)

################################################################

def reportable_entries(entries, date_start, date_end=None, posted_start=None):
    def date_in_period(ntry):
        my_date = ntry.date()
        date_after_start = date.ge(my_date, date_start)
        date_before_end = date_end is None or date.le(my_date, date_end)
        return date_after_start and date_before_end
    def posted_in_period(ntry):
        my_date = ntry.date()
        my_posted = ntry.posted()
        date_before_start = date.lt(my_date, date_start)
        posted_late = date.ge(my_posted, posted_start or date_start)
        return date_before_start and posted_late
    return [ntry for ntry in entries
            if date_in_period(ntry) or posted_in_period(ntry)]

def material_entries(entries, amt="100"):
    return [ntry for ntry in entries
            if amount.ge(ntry.credit() or ntry.debit(), amt)]

################################################################
