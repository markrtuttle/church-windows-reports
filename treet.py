#!/usr/bin/env python

import accountt

################################################################

# tree: strip accounts types
# tree: max depth
# tree accumlate account types

# prune: number -> level -> boolean

################################################################

def max0(numbers):
    return max(numbers + [0])

class Node(object):
    def __init__(self, number, name):
        self.number_ = number
        self.name_ = name
        self.period_activity_ = 0
        self.year_activity_ = 0
        self.initial_balance_ = 0
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

    def period_activity(self):
        return self.period_activity_

    def year_activity(self):
        return self.year_activity_

    def initial_balance(self):
        return self.initial_balance_

    def balance(self):
        return self.balance_

    def budget(self):
        return self.budget_

    def type(self):
        return self.type_

    def kind(self):
        return self.kind_

    def set_period_activity(self, activity):
        self.period_activity_ = activity

    def set_year_activity(self, activity):
        self.year_activity_ = activity

    def set_initial_balance(self, initial):
        self.initial_balance_ = initial

    def set_balance(self, balance):
        self.balance_ = balance

    def set_budget(self, budget):
        self.budget_ = budget

    def copy(self):
        node = Node(self.number(), self.name())
        node.set_period_activity(self.period_activity())
        node.set_year_activity(self.year_activity())
        node.set_initial_balance(self.initial_balance())
        node.set_balance(self.balance())
        node.set_budget(self.budget())

        return node

class Tree(object):

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
            children = [num for num in chart.accounts()
                        if chart.account(num).parent() is None]
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

    def set_initial_balances(self, initial):
        self.node().set_initial_balance(initial.balance(self.node().number()))
        for subtree in self.subtrees():
            subtree.set_initial_balances(initial)

    def set_balances(self, period_credit, period_debit, year_credit, year_debit):
        number = self.node().number()
        period_activity = period_credit.get(number, 0) - period_debit.get(number, 0)
        year_activity = year_credit.get(number, 0) - year_debit.get(number, 0)

        if self.node().kind() == "D":
            period_activity = -period_activity
            year_activity = -year_activity

        balance = self.node().initial_balance() + year_activity
        for subtree in self.subtrees():
            subtree.set_balances(period_credit, period_debit, year_credit, year_debit)

            if self.node().kind() == subtree.node().kind():
                period_activity += subtree.node().period_activity()
                year_activity += subtree.node().year_activity()
                balance += subtree.node().balance()
            else:
                period_activity -= subtree.node().period_activity()
                year_activity -= subtree.node().year_activity()
                balance -= subtree.node().balance()

        self.node().set_period_activity(period_activity)
        self.node().set_year_activity(year_activity)
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
            if remove(number) or max_level is not None and level+1 > max_level:
                continue
            subtree.remove_from_tree(remove, level+1, max_level)
            subtrees.append(subtree)
        self.subtrees_ = subtrees
        self.depth_ = max0([stree.depth() for stree in self.subtrees()]) + 1
        self.traversal_ = None

    def remove_income_expense_from_tree(self):
        def remove(number):
            return (accountt.is_income_number(number) or
                    accountt.is_expense_number(number))
        self.remove_from_tree(remove)

class Forest(object):
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
