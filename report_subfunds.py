#!/usr/bin/env python3

import summary


def subfund_report(period_name, forest, layout):
    for name in ["Special Funds", "Investment Return", "PSCC Legacy Projects", "Capital Improvement Projects"]:
        tree = forest.tree_name(name).copy()
        tree.remove_income_expense_from_tree()
        summary.tree_summary(tree, name, period_name, period_name, zeros=False, layout=layout)
        print()
