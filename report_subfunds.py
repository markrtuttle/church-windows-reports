#!/usr/bin/env python

import treet
import summary

def subfund_report(period_name, tree, chart, balance, width):

    name = "Special Funds"
    number = chart.number(name)
    subtree = treet.remove_income_expense_from_tree(tree.tree(number))
    summary.tree_summary(subtree, chart, balance, name, period_name, period_name, zeros=False)

    print

    name = "Investment Return"
    number = chart.number(name)
    subtree = treet.remove_income_expense_from_tree(tree.tree(number))
    summary.tree_summary(subtree, chart, balance, name, period_name, period_name, zeros=False)
