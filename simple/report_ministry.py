#!/usr/bin/env python

import amountt
import datet

import report_style
from utility import truncate

################################################################

def ministry_reports(journal, balance, chart, budget, ministry, period_name,
                     date_start, date_end, posted_start, posted_end,
                     width=80):

    # pylint: disable=too-many-arguments

    names = ministry.keys()
    names.sort(key=ministry.name)

    first = True
    for name in names:
        if not first:
            print "\f"
        first = False

        print "{} ministry ({} to {})".format(ministry.name(name),
                                              datet.to_string(date_start),
                                              datet.to_string(date_end))
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
    report_style.account_report("General Fund", period_name, numbers,
                                chart, balance, budget,
                                width, name_w, amount_w, balance_w, name_max)

    print
    numbers = ministry.funds(name)
    report_style.fund_report("Other Funds", period_name, numbers,
                             chart, balance,
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

    remaining_width = width - (name_w + 1 + amount_w + 1 + 5 + 1 + comment_w)
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width / 10 * 4
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    comment_w += remaining_width - name_pad

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
    entries.sort(key=lambda entry: (entry.name(), entry.date()))

    for entry in entries:
        (month, day, _) = datet.parse_ymd_string(entry.date())

        amount = (entry.debit() or 0) - (entry.credit() or 0)
        if chart.account(entry.number()).is_credit_account():
            amount = -amount


        print ("{3:<{nw}} {4:>{aw}} {0:>2}/{1:>2} {2:<{cw}}"
               .format(month, day,
                       truncate(entry.comment(), comment_w),
                       truncate(entry.name(), name_w),
                       truncate(amountt.to_string(amount), amount_w),
                       cw=comment_w,
                       nw=name_w,
                       aw=amount_w))

################################################################
