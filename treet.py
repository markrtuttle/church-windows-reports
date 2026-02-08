#!/usr/bin/env python3

import accountt

################################################################

# tree: strip accounts types
# tree: max depth
# tree accumlate account types

# prune: number -> level -> boolean

################################################################


def max0(numbers):
    return max(numbers + [0])


class Node:
    def __init__(self, number, name):
        self.number_ = number
        self.name_ = name

        self.early_credit_ = 0
        self.early_debit_ = 0
        self.early_activity_ = 0

        self.period_start_ = 0
        self.period_credit_ = 0
        self.period_debit_ = 0
        self.period_activity_ = 0

        self.year_start_ = 0
        self.year_credit_ = 0
        self.year_debit_ = 0
        self.year_activity_ = 0

        self.balance_ = 0
        self.budget_ = 0

        self.type_ = number[:1]
        if self.type_ not in ["0", "1", "2", "3", "4", "5"]:
            self.type_ = "2"
        self.kind_ = "D" if self.type_ in ["0", "1", "5"] else "C"

    def number(self):
        return self.number_

    def name(self):
        return self.name_

    def early_credit(self):
        return self.early_credit_

    def early_debit(self):
        return self.early_debit_

    def early_activity(self):
        return self.early_activity_

    def period_start(self):
        return self.period_start_

    def period_credit(self):
        return self.period_credit_

    def period_debit(self):
        return self.period_debit_

    def period_activity(self):
        return self.period_activity_

    def year_start(self):
        return self.year_start_

    def year_debit(self):
        return self.year_debit_

    def year_credit(self):
        return self.year_credit_

    def year_activity(self):
        return self.year_activity_

    def balance(self):
        return self.balance_

    def budget(self):
        return self.budget_

    def type(self):
        return self.type_

    def kind(self):
        return self.kind_

    def set_early_credit(self, credit):
        self.early_credit_ = credit

    def set_early_debit(self, debit):
        self.early_debit_ = debit

    def set_early_activity(self, activity):
        self.early_activity_ = activity

    def set_period_start(self, start):
        self.period_start_ = start

    def set_period_credit(self, credit):
        self.period_credit_ = credit

    def set_period_debit(self, debit):
        self.period_debit_ = debit

    def set_period_activity(self, activity):
        self.period_activity_ = activity

    def set_year_start(self, start):
        self.year_start_ = start

    def set_year_credit(self, credit):
        self.year_credit_ = credit

    def set_year_debit(self, debit):
        self.year_debit_ = debit

    def set_year_activity(self, activity):
        self.year_activity_ = activity

    def set_balance(self, balance):
        self.balance_ = balance

    def set_budget(self, budget):
        self.budget_ = budget

    def copy(self):
        node = Node(self.number(), self.name())

        node.set_period_start(self.period_start())
        node.set_period_credit(self.period_credit())
        node.set_period_debit(self.period_debit())
        node.set_period_activity(self.period_activity())

        node.set_year_start(self.year_start())
        node.set_year_credit(self.year_credit())
        node.set_year_debit(self.year_debit())
        node.set_year_activity(self.year_activity())

        node.set_balance(self.balance())
        node.set_budget(self.budget())

        return node


class Tree:
    def __init__(self, chart=None, number=None):
        if chart is None:
            self.node_ = None
            self.subtrees_ = None
            self.depth_ = None
            self.traversal_ = None
            return

        if number is None:
            number = "0.000.000.000"
            name = "Root"
            children = [num for num in chart.accounts() if chart.account(num).parent() is None]
        else:
            name = chart.account(number).name()
            children = chart.account(number).children()
        children = sorted(children, key=lambda number: chart.account(number).name())

        numbers = []
        numbers += [num for num in children if accountt.is_asset_number(num)]
        numbers += [num for num in children if accountt.is_liability_number(num)]
        numbers += [num for num in children if accountt.is_fund_number(num)]
        numbers += [num for num in children if accountt.is_income_number(num)]
        numbers += [num for num in children if accountt.is_expense_number(num)]
        numbers += [num for num in children if accountt.is_vendor_number(num)]

        self.node_ = Node(number, name)
        self.subtrees_ = [Tree(chart, num) for num in numbers]

        depths = [subtree.depth() for subtree in self.subtrees_]
        self.depth_ = max(depths + [0]) + 1

        traversals = [subtree.traversal() for subtree in self.subtrees_]
        traversal = [num for traversal in traversals for num in traversal]
        self.traversal_ = traversal + [number]

    def node(self):
        return self.node_

    def subtrees(self):
        return self.subtrees_

    def depth(self):
        return self.depth_

    def traversal(self):
        return self.traversal_

    def set_year_starts(self, initial):
        year_start = initial.balance(self.node().number())
        for subtree in self.subtrees():
            subtree.set_year_starts(initial)
            if self.node().kind() == subtree.node().kind():
                year_start += subtree.node().year_start()
            else:
                year_start -= subtree.node().year_start()
        self.node().set_year_start(year_start)

    def set_balances(self, early_credit, early_debit, period_credit, period_debit, year_credit, year_debit):
        number = self.node().number()

        ecredit = early_credit.get(number, 0)
        edebit = early_debit.get(number, 0)
        pcredit = period_credit.get(number, 0)
        pdebit = period_debit.get(number, 0)
        ycredit = year_credit.get(number, 0)
        ydebit = year_debit.get(number, 0)

        for subtree in self.subtrees():
            subtree.set_balances(early_credit, early_debit, period_credit, period_debit, year_credit, year_debit)

            ecredit += subtree.node().early_credit()
            edebit += subtree.node().early_debit()
            pcredit += subtree.node().period_credit()
            pdebit += subtree.node().period_debit()
            ycredit += subtree.node().year_credit()
            ydebit += subtree.node().year_debit()

        assert ycredit == ecredit + pcredit
        assert ydebit == edebit + pdebit

        self.node().set_early_credit(ecredit)
        self.node().set_early_debit(edebit)
        self.node().set_period_credit(pcredit)
        self.node().set_period_debit(pdebit)
        self.node().set_year_credit(ycredit)
        self.node().set_year_debit(ydebit)

        sign = 1 if self.node().kind() == "C" else -1
        early_activity = sign * (ecredit - edebit)
        period_activity = sign * (pcredit - pdebit)
        year_activity = sign * (ycredit - ydebit)

        assert year_activity == early_activity + period_activity

        self.node().set_early_activity(early_activity)
        self.node().set_period_activity(period_activity)
        self.node().set_year_activity(year_activity)

        year_start = self.node().year_start()
        period_start = year_start + early_activity
        balance = year_start + year_activity

        assert balance == period_start + period_activity
        assert balance == year_start + year_activity

        self.node().set_period_start(period_start)
        self.node().set_balance(balance)

    def set_budgets(self, budget):
        number = self.node().number()

        total = budget.balance(number)
        for subtree in self.subtrees():
            subtree.set_budgets(budget)

            if subtree.node().budget() is not None:
                if self.node().kind() == subtree.node().kind():
                    total = (total or 0) + subtree.node().budget()
                else:
                    total = (total or 0) - subtree.node().budget()

        self.node().set_budget(total)

    def copy(self):
        tree = Tree()
        tree.node_ = self.node().copy()
        tree.subtrees_ = [subtree.copy() for subtree in self.subtrees()]
        tree.depth_ = self.depth()
        tree.traversal_ = self.traversal()
        return tree

    def remove_from_tree(self, remove=lambda num: False, level=0, max_level=None):
        number = self.node().number()
        if remove(number) or max_level is not None and level > max_level:
            raise UserWarning

        subtrees = []
        for subtree in self.subtrees():
            number = subtree.node().number()
            if remove(number) or max_level is not None and level + 1 > max_level:
                continue
            subtree.remove_from_tree(remove, level + 1, max_level)
            subtrees.append(subtree)
        self.subtrees_ = subtrees
        self.depth_ = max0([stree.depth() for stree in self.subtrees()]) + 1
        self.traversal_ = None

    def remove_income_expense_from_tree(self):
        def remove(number):
            return accountt.is_income_number(number) or accountt.is_expense_number(number)

        self.remove_from_tree(remove)


class Forest:
    def __init__(self, tree):
        self.number_ = {}
        self.name_ = {}

        def set_trees(tree):
            self.number_[tree.node().number()] = tree
            self.name_[tree.node().name()] = tree
            for subtree in tree.subtrees():
                set_trees(subtree)

        set_trees(tree)

    def tree_number(self, number):
        return self.number_.get(number)

    def tree_name(self, name):
        return self.name_.get(name)
