#!/usr/bin/env python3

import summary
import summary_budget

import detail
import entriest

################################################################


def ministry_reports(forest, entries, ministry, period_name, layout=None):
    # pylint: disable=too-many-arguments

    names = list(ministry.keys())
    names.sort()

    first = True
    for name in names:
        if not first:
            print("\f")
        first = False

        print(f"{ministry.name(name)} ministry")
        # print "Deacons: {}".format(', '.join(ministry.deacons(name)))
        print()
        ministry_summary(name, forest, ministry, period_name, layout)
        print()
        ministry_detail(name, entries, ministry, layout)


################################################################


def ministry_summary(name, forest, ministry, period_name, layout):
    # pylint: disable=too-many-arguments

    numbers = ministry.accounts(name)
    trees = [forest.tree_number(num) for num in numbers]
    if trees:
        summary_budget.tree_summaries(
            trees, report_name="General Fund", activity_name=period_name, zeros=False, layout=layout
        )

    if numbers:
        print()

    numbers = ministry.funds(name)
    trees = [forest.tree_number(num).copy() for num in numbers]
    for tree in trees:
        tree.remove_income_expense_from_tree()
    if trees:
        summary.tree_summaries(
            trees,
            report_name="Other Funds",
            period_name=period_name,
            balance_name=period_name,
            zeros=False,
            layout=layout,
        )


################################################################


def ministry_detail(name, entries, ministry, layout):
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    numbers = ministry.accounts(name) + ministry.funds_accounts(name)

    entries = entriest.select_by_number(entries, numbers)
    groups = entriest.group_by_month(entries, reverse=True)
    groups = [entriest.sort_by_amount(group, reverse=True) for group in groups]
    groups = [entriest.sort_by_name(group) for group in groups]

    for group in groups:
        print()
        detail.detail(group, credit=True, layout=layout)


################################################################
