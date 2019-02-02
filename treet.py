#!/usr/bin/env python

import accountt

################################################################

def build_tree(number, chart):
    account = chart.account(number)

    nums = []
    nums += account.assets(chart)
    nums += account.liabilities(chart)
    nums += account.funds(chart)
    nums += account.incomes(chart)
    nums += account.expenses(chart)
    nums += account.vendors(chart)

    return (number, build_trees(nums, chart))

def build_trees(numbers, chart):
    return [build_tree(num, chart) for num in numbers]

################################################################

def depth(tree):
    (_, subtrees) = tree
    return depths(subtrees) + 1

def depths(trees):
    if not trees:
        return 0
    return max([depth(tree) for tree in trees])

################################################################

# tree: strip accounts types
# tree: max depth
# tree accumlate account types

# prune: number -> level -> boolean

def remove_from_tree(tree, remove=lambda num: False, level=0, max_level=None):
    (number, subtrees) = tree
    if remove(number) or max_level is not None and level > max_level:
        return None
    return (number, remove_from_trees(subtrees, remove, level+1, max_level))

def remove_from_trees(trees, remove, level=0, max_level=None):
    trees = [remove_from_tree(tree, remove, level, max_level) for tree in trees]
    return [tree for tree in trees if tree is not None]

def select_from_tree(tree, select):
    (number, subtrees) = tree
    node = [number] if select(number) else []
    return node + select_from_trees(subtrees, select)

def select_from_trees(trees, select):
    node_lists = [select_from_tree(tree, select) for tree in trees]
    return [node for node_list in node_lists for node in node_list]

def remove_income_expense_from_tree(tree):
    def remove(number):
        return (accountt.is_income_number(number) or
                accountt.is_expense_number(number))
    return remove_from_tree(tree, remove)

def select_income_expense_from_tree(tree):
    def select(number):
        return (accountt.is_income_number(number) or
                accountt.is_expense_number(number))
    return select_from_tree(tree, select)

################################################################

def walk_tree(tree):
    (number, subtrees) = tree
    return walk_trees(subtrees) + [number]

def walk_trees(trees):
    return [number
            for walk in [walk_tree(tree) for tree in trees]
            for number in walk]

################################################################

class Tree(object):

    def __init__(self, chart):
        roots = [number
                 for number in chart.accounts()
                 if chart.account(number).parent() is None]
        roots = sorted(roots, key=lambda number: chart.account(number).name())

        numbers = []
        numbers += [num for num in roots if accountt.is_asset_number(num)]
        numbers += [num for num in roots if accountt.is_liability_number(num)]
        numbers += [num for num in roots if accountt.is_fund_number(num)]
        numbers += [num for num in roots if accountt.is_income_number(num)]
        numbers += [num for num in roots if accountt.is_expense_number(num)]
        numbers += [num for num in roots if accountt.is_vendor_number(num)]

        root_trees = build_trees(numbers, chart)

        self.tree_ = {}

        def install_tree(tree):
            (number, subtrees) = tree
            self.tree_[number] = tree
            install_trees(subtrees)

        def install_trees(trees):
            for tree in trees:
                install_tree(tree)

        self.tree_[None] = (None, root_trees)
        install_trees(root_trees)

    def tree(self, number):
        return self.tree_[number]

    def depth(self, number):
        return depth(self.tree_[number])

    def walk(self, number):
        (_, subtrees) = self.tree_[number]
        subwalk = walk_trees(subtrees)
        if number is None:
            return subwalk
        return subwalk + [number]

    def root(self):
        return self.tree(None)

    def root_walk(self):
        return self.walk(None)
