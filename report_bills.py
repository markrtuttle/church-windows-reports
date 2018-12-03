#!/usr/bin/env python

import amountt
import entryt
import report_style

def bills_report(chart, journal,
                 date_start, date_end, posted_start, posted_end,
                 width=80,
                 comment_w=35,
                 name_w=25,
                 amount_w=8,
                 name_max=40,
                 min_amount=amountt.from_string("200.00")):

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
                (posted_start and posted_end
                 and
                 entry.posted_is(posted_start, posted_end)
                 and
                 entry.date_is(None, posted_end)))]


    report_style.display_entries(entries, chart, True, ["reverse_amount"],
                                 width, comment_w, name_w, amount_w,
                                 name_max)
