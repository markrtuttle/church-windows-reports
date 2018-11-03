#!/usr/bin/env python

import amountt
import datet
import entryt
from utility import truncate


def prepare_entries(journal, chart,
                    date_start, date_end, posted_start, posted_end,
                    min_amount=None):

    # pylint: disable=too-many-arguments

    entries = [entry for entry in journal.entries()
               if
               entry.type() == entryt.BILL
               and
               chart.account(entry.number()).is_debit_account()
               and
               (entry.debit_is(min_amount, None)
                or
                entry.credit_is(min_amount, None))
               and
               (entry.date_is(date_start, date_end)
                or
                (entry.posted_is(posted_start, posted_end)
                 and
                 entry.date_is(None, posted_end)))]

    partition = {mon: [] for mon in range(1, 13)}
    for entry in entries:
        (month, _, _) = datet.parse_ymd_string(entry.date())
        partition[month].append(entry)

    for month in range(1, 13):
        partition[month].sort(key=lambda entry:
                              (-(entry.debit() or entry.credit()),
                               entry.name(),
                               entry.date()))

    return partition

def display_entries(partition, chart,
                    width, comment_w, name_w, amount_w, name_max):

    # pylint: disable=too-many-arguments

    remaining_width = width - (name_w + 1 + amount_w + 1 + 5 + 1 + comment_w)
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width / 10 * 4
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    comment_w += remaining_width - name_pad

    printed = False
    for month in range(12, 0, -1):
        if not partition[month]:
            continue

        if printed:
            print
        printed = True

        for entry in partition[month]:
            (month, day, _) = datet.parse_ymd_string(entry.date())

            amount = chart.account(entry.number()).amount(entry.debit(),
                                                          entry.credit())

            print ("{4:>{aw}} {0:>2}/{1:>2} {3:<{nw}} {2:<{cw}}"
                   .format(month, day,
                           truncate(entry.comment(), comment_w),
                           truncate(entry.name(), name_w),
                           truncate(amountt.to_string(amount), amount_w),
                           cw=comment_w,
                           nw=name_w,
                           aw=amount_w))

def bills_report(journal, chart,
                 date_start, date_end, posted_start, posted_end,
                 width=80,
                 comment_w=35,
                 name_w=25,
                 amount_w=8,
                 name_max=40,
                 min_amount=amountt.from_string("200.00")):

    # pylint: disable=too-many-arguments

    entries = prepare_entries(journal, chart,
                              date_start, date_end, posted_start, posted_end,
                              min_amount)

    display_entries(entries, chart,
                    width, comment_w, name_w, amount_w, name_max)
