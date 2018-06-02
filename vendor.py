#!/usr/bin/env python

# pylint: disable=missing-docstring

import csv

import amount
import statement

class Vendor(object):
    # pylint: disable=too-few-public-methods

    def __init__(self, filename):
        self.vendor = {}
        with open(filename, 'r') as handle:
            name = None
            amt = None
            for line in csv.reader(handle):
                line += ['', '', '', '', '', '', '', '', '', '']
                name_ = line[1]
                amt_ = line[9]
                if name_ or amt_:
                    if name and amt:
                        self.vendor[name] = amt
                    if name_:
                        name = name_
                        amt = None
                        continue
                    if amt_ and not amount.eq(amt_, "0"):
                        amt = amount.fmt(amt_)

    def report(self, jnl, arg):
        entries = jnl.period_entries(arg.date_start,
                                     arg.date_end,
                                     arg.posted_start)
        for name in self.vendor:
            ents = [ent for ent in entries if ent.name() == name]
            print "\n", name, self.vendor[name]
            statement.journal_statement(None, jnl, arg.line_width,
                                        None, ents,
                                        is_debit_account=False)
