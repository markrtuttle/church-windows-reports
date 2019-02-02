#!/usr/bin/env python

import entriest
import detail
import amountt

def bills_report(chart, journal,
                 date_start, date_end, posted_start, posted_end,
                 width=80,
                 comment_w=35,
                 name_w=25,
                 amount_w=8,
                 name_max=40,
                 min_amount=amountt.from_string("100.00")):

    entries = journal.entries()
    entries = entriest.select_by_date(entries, date_start, date_end,
                                      posted_start, posted_end)
    entries = entriest.select_by_amount(entries, low="100.00")
    entries = entriest.select_bill(entries)
    entries = entriest.select_debit(entries)
    groups = entriest.group_by_month(entries, reverse=True)
    groups = [entriest.sort_by_amount(group, reverse=True) for group in groups]

    for group in groups:
        print
        detail.detail(group, credit=False, width=width,
                      comment_w=comment_w, name_w=name_w, amount_w=amount_w,
                      name_max=name_max)
