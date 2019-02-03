#!/usr/bin/env python

import datet

import summary
import summary_budget

import detail
import entriest

import treet

################################################################

def ministry_reports(chart, tree, journal, budget, balance, ministry, period_name,
                     date_start, date_end, posted_start, posted_end, layout=None):

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
        ministry_summary(name, period_name, tree, balance, chart, budget, ministry,
                         layout)
        print
        ministry_detail(name, journal, chart, ministry,
                        date_start, date_end, posted_start, posted_end,
                        layout)

################################################################

def ministry_summary(name, period_name, tree, balance, chart, budget, ministry,
                     layout):

    # pylint: disable=too-many-arguments

    numbers = ministry.accounts(name)
    trees = [tree.tree(num) for num in numbers]
    if trees:
        summary_budget.tree_summaries(trees, chart, balance, budget,
                                      report_name="General Fund", activity_name=period_name,
                                      layout=layout)

    if numbers:
        print

    numbers = ministry.funds(name)
    trees = [tree.tree(num) for num in numbers]
    trees = [treet.remove_income_expense_from_tree(tree) for tree in trees]
    if trees:
        summary.tree_summaries(trees, chart, balance,
                               report_name="Other Funds", activity_name=period_name,
                               balance_name=period_name,
                               layout=layout)

################################################################

def ministry_detail(name, journal, chart, ministry,
                    date_start, date_end, posted_start, posted_end,
                    layout):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    numbers = ministry.accounts(name) + ministry.funds_accounts(name)
    entries = [entry for entry in journal.entries()
               if
               entry.number_is(numbers)
               and
               (entry.date_is(date_start, date_end)
                or
                (posted_start and posted_end
                 and
                 entry.posted_is(posted_start, posted_end)
                 and
                 entry.date_is(None, posted_end)))]

    entries = journal.entries()
    entries = entriest.select_by_number(entries, numbers)
    entries = entriest.select_by_date(entries, date_start, date_end,
                                      posted_start, posted_end)
    groups = entriest.group_by_month(entries, reverse=True)
    groups = [entriest.sort_by_amount(group, reverse=True) for group in groups]
    groups = [entriest.sort_by_name(group, chart) for group in groups]

    for group in groups:
        print
        detail.detail(group, credit=True, layout=layout)

################################################################
