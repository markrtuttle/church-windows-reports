#!/usr/bin/env python

import amountt
import report_style

import entriest
import detail

def vendor_report(chart, journal, balance,
                  date_start, date_end,
                  all_vendors=False,
                  width=80,
                  comment_w=35,
                  name_w=25,
                  amount_w=8,
                  name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    vendor_numbers = chart.account(chart.vendor_number()).children()

    numbers = [number for number in vendor_numbers if
               balance.current(number) or all_vendors]

    first = True
    for number in numbers:
        entries = journal.entries()
        entries = entriest.select_by_number(entries, [number])
        entries = entriest.select_by_date(entries, date_start, date_end)
        if not entries and not balance.current(number):
            continue

        if not first:
            print
        first = False

        print "{}: balance {} (prior balance {})".format(
            chart.account(number).name(),
            amountt.to_string(balance.current(number)),
            amountt.to_string(balance.prior(number)))
        detail.detail(entries, credit=True,
            width=width, comment_w=comment_w, name_w=name_w, amount_w=amount_w,
            name_max=name_max)
