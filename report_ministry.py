#!/usr/bin/env python

import datet
import report_style

################################################################

def ministry_reports(chart, journal, budget, balance, ministry, period_name,
                     date_start, date_end, posted_start, posted_end,
                     width=80):

    # pylint: disable=too-many-arguments

    names = ministry.keys()
    names.sort()

    first = True
    for name in names:
        if not first:
            print "\f"
        first = False

        print "{} ministry ({} to {})".format(ministry.name(name),
                                              datet.to_string(date_start),
                                              datet.to_string(date_end))
        print "Deacons: {}".format(', '.join(ministry.deacons(name)))
        print
        ministry_summary(name, period_name, balance, chart, budget, ministry,
                         width=width)
        print
        ministry_detail(name, journal, chart, ministry,
                        date_start, date_end, posted_start, posted_end,
                        width=width)

################################################################

def ministry_summary(name, period_name, balance, chart, budget, ministry,
                     width=80,
                     name_w=21,
                     amount_w=8,
                     balance_w=10,
                     name_max=40):

    # pylint: disable=too-many-arguments

    numbers = ministry.accounts(name)
    report_style.display_budgeted_accounts(
        "General Fund", period_name, numbers, chart, balance, budget,
        width, name_w, amount_w, balance_w, name_max)

    if numbers:
        print

    numbers = ministry.funds(name)
    report_style.display_accounts(
        "Other Funds", period_name, numbers, chart, balance,
        width, name_w, amount_w, balance_w, name_max)

################################################################

def ministry_detail(name, journal, chart, ministry,
                    date_start, date_end, posted_start, posted_end,
                    width=80,
                    comment_w=35,
                    name_w=25,
                    amount_w=8,
                    name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    numbers = ministry.accounts(name) + ministry.funds_accounts(name)
    entries = [entry for entry in journal.entries()
               if
               entry.number_is(numbers)
               and
               (entry.date_is(date_start, date_end)
                or
                (entry.posted_is(posted_start, posted_end)
                 and
                 entry.date_is(None, posted_end)))]

    report_style.display_entries(entries, chart,
                                 group_by_month=False,
                                 sort_keys=['name', 'reverse_amount', 'date'],
                                 width=width,
                                 comment_w=comment_w,
                                 name_w=name_w,
                                 amount_w=amount_w,
                                 name_max=name_max)

################################################################
