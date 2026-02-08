#!/usr/bin/env python3

import amountt
import detail


def vendor_report(forest, entries, layout=None, all_vendors=False):
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    trees = forest.tree_number("2.000.000.000").subtrees()

    first = True
    for tree in trees:
        number = tree.node().number()
        details = [entry for entry in entries if entry.number_is([number]) or all_vendors]
        if not details and not tree.node().balance():
            continue

        if not first:
            print()
        first = False

        print(
            "{}: prior balance {}, balance {}".format(
                tree.node().name(),
                amountt.to_string(tree.node().balance() - tree.node().period_activity()),
                amountt.to_string(tree.node().balance()),
            )
        )
        detail.detail(details, credit=True, layout=layout)
