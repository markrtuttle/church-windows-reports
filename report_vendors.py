#!/usr/bin/env python

import amountt
import report_style

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
        entries = [entry for entry in journal.entries() if
                   entry.number() == number
                   and
                   entry.date_is(date_start, date_end)]

        if not entries and not balance.current(number):
            continue

        if not first:
            print
        first = False

        print "{}: balance {} (prior balance {})".format(
            chart.account(number).name(),
            amountt.to_string(balance.current(number)),
            amountt.to_string(balance.prior(number)))
        report_style.display_entries(
            entries, chart,
            width=width, comment_w=comment_w, name_w=name_w, amount_w=amount_w,
            name_max=name_max)
