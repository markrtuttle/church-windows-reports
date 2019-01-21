#!/usr/bin/env python

import accountt
import amountt
import datet

################################################################

def build_tree(number, chart):
    account = chart.account(number)

    nums = []
    nums += account.assets(chart)
    nums += account.liabilities(chart)
    nums += account.funds(chart)
    nums += account.incomes(chart)
    nums += account.expenses(chart)

    return (number, build_trees(nums, chart))

def build_trees(numbers, chart):
    return [build_tree(num, chart) for num in numbers]

################################################################

def depth(tree):
    (_, subtrees) = tree
    if not subtrees:
        return 1
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

def remove_from_tree(tree, remove, level=0, max_level=None):
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

def make_summary_format(width=80,
                        name_w=25, amount_w=8, balance_w=10,
                        name_max=40, level_max=0):

    name_w += 2*level_max
    amount_w += 2*level_max
    balance_w += 2*level_max

    format_string = "| {{:<{nw}}} | {{:>{aw}}} | {{:>{bw}}} |"
    format_length = lambda: 2 + name_w + 3 + amount_w + 3 + balance_w + 2

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad

    string = format_string.format(nw=name_w, aw=amount_w, bw=balance_w)
    width = format_length()

    def print_line(name, activity, balance, level=0):
        name = " "*(2*level) + name
        name = name[:name_w]
        act = amountt.to_string(activity) + " "*(2*level)
        bal = amountt.to_string(balance)  + " "*(2*level)
        print string.format(name, act, bal)

    def print_rule():
        print '-'*width

    return (print_line, print_rule)

def tree_summary_line(tree, chart, balance, level, print_line):

    (number, trees) = tree

    name = chart.account(number).name()
    activity = balance.activity(number)
    current = balance.current(number)

    print_line(name, activity, current, level)
    tree_summary_lines(trees, chart, balance, level+1, print_line)

def tree_summary_lines(trees, chart, balance, level, print_line):
    for tree in trees:
        tree_summary_line(tree, chart, balance, level, print_line)

def tree_summary(tree, chart, balance):
    (line, rule) = make_summary_format(level_max=depth(tree))
    rule()
    tree_summary_line(tree, chart, balance, 0, line)
    rule()

def tree_summaries(trees, chart, balance):
    (line, rule) = make_summary_format(level_max=max([depth(tree) for tree in trees]))
    rule()
    tree_summary_lines(trees, chart, balance, 0, line)
    rule()

################################################################

def make_detail_format(width=80,
                       comment_w=35, name_w=25, amount_w=8,
                       name_max=40):

    format_string = "{{:>{aw}}} {{:>2}}/{{:>2}} {{:<{nw}}} {{:<{cw}}}"
    format_length = lambda: amount_w + 1 + 5 + 1 + name_w + 1 + comment_w

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width / 10 * 4
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    comment_w += remaining_width - name_pad

    string = format_string.format(aw=amount_w, nw=name_w, cw=comment_w)
    width = format_length()

    def print_line(amount, date, name, comment):
        amount = amountt.to_string(amount)
        (month, day, _) = datet.parse_ymd_string(date)
        name = name[:name_w]
        comment = comment[:comment_w]
        print string.format(amount, month, day, name, comment)

    def print_rule():
        print '-'*width

    return (print_line, print_rule)

def entry_line(entry, print_line, credit):
    date = entry.date()
    name = entry.name()
    comment = entry.comment()

    if credit:
        amount = (entry.credit() or 0) - (entry.debit() or 0)
    else:
        amount = (entry.debit() or 0) - (entry.credit() or 0)

    print_line(amount, date, name, comment)

def entry_lines(entries, print_line, credit):
    for entry in entries:
        entry_line(entry, print_line, credit)

def detail(entries, credit=True):
    (print_line, _) = make_detail_format()
    entry_lines(entries, print_line, credit)

################################################################

def walk_tree(tree):
    (number, subtrees) = tree
    return walk_trees(subtrees) + [number]

def walk_trees(trees):
    return [number
            for walk in [walk_tree(tree) for tree in trees]
            for number in walk]

def walk_chart(chart):
    numbers = [number
               for number in chart.accounts()
               if chart.account(number).parent() is None]
    return walk_trees(build_trees(numbers, chart))

################################################################
