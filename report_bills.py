#!/usr/bin/env python3

import entriest
import detail

def bills_report(entries, layout, min_amount="100.00"):

    entries = entriest.select_by_amount(entries, low=min_amount)
    entries = entriest.select_bill(entries)
    entries = entriest.select_debit(entries)
    groups = entriest.group_by_month(entries, reverse=True)
    groups = [entriest.sort_by_amount(group, reverse=True) for group in groups]

    for group in groups:
        print()
        detail.detail(group, credit=False, layout=layout)
