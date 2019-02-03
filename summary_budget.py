#!/usr/bin/env python

import treet
import amountt
import accountt
import layoutt

################################################################

def make_summary_format(layout=None, level_max=0):

    if layout is None:
        layout = layoutt.Layout()

    width = layout.width()
    name_w = layout.name()
    amount_w = layout.amount()
    balance_w = layout.balance()
    name_max = layout.name_max()

    name_w += 2*level_max
    amount_w += 2*level_max
    balance_w += 2*level_max

    format_string = ("| {{:<{nw}}} | {{:>{aw}}} "
                     "| {{:>{bw}}} {{:>{bw}}} {{:>{bw}}} {{:>{aw}}} |")
    format_length = lambda: (2 + name_w + 3 + amount_w + 3 +
                             3*(balance_w + 1) + amount_w + 2)

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad

    string = format_string.format(nw=name_w, aw=amount_w, bw=balance_w)
    width = format_length()

    def print_line(name="", activity="", budget="", spent="", left="", percent="", level=0):
        name = " "*(2*level) + name
        name = name[:name_w]
        act = activity + " "*(2*level)
        bud = budget + " "*(2*level)
        spn = spent + " "*(2*level)
        lft = left  + " "*(2*level)
        pct = percent + " "*(2*level)
        print string.format(name, act, bud, spn, lft, pct)

    def print_amounts(name, activity, budget, spent, level=0):
        act = amountt.to_string(activity)
        bud = amountt.to_string(budget)
        spn = amountt.to_string(spent)
        left = budget-spent
        percent = float(left)/float(budget) if budget else 0
        lft = amountt.to_string(left)
        pct = "{:.2f}".format(percent)
        print_line(name, act, bud, spn, lft, pct, level)

    def print_rule():
        print '-'*width

    return (print_line, print_amounts, print_rule)

def tree_summary_line(tree, level,
                      print_line, print_amounts, zeros, credit_tree):

    number = tree.node().number()
    name = tree.node().name()
    activity = tree.node().period_activity()
    current = tree.node().balance()
    budget = tree.node().budget() or 0

#    if credit_tree != accountt.is_credit_number(number):
#        activity = -activity
#        current = -current

    if zeros or activity or current or budget:
        print_amounts(name, activity, budget, current, level)
    tree_summary_lines(tree.subtrees(), level+1,
                       print_line, print_amounts, zeros, credit_tree)

def tree_summary_lines(trees, level,
                       print_line, print_amounts, zeros, credit_tree):
    last_kind = None
    for tree in trees:
        this_kind = tree.node().type()
        if last_kind and last_kind != this_kind:
            print_line()
        last_kind = this_kind
        tree_summary_line(tree, level,
                          print_line, print_amounts, zeros, credit_tree)

def header(line, rule, report_name="", activity_name=""):
    rule()
    line("", activity_name, "Budget", "Budget", "Budget", "Percent")
    line(report_name, "activity", "total", "spent", "left", "left")
    rule()

def footer(rule):
    rule()

def tree_summary(tree, 
                 report_name="", activity_name="", zeros=True,
                 credit_tree=True, layout=None):
    (fmt, line, rule) = make_summary_format(layout, tree.depth())
    header(fmt, rule, report_name, activity_name)
    tree_summary_line(tree, 0, fmt, line, zeros, credit_tree)
    footer(rule)

def tree_summaries(trees, 
                   report_name=None, activity_name=None, zeros=True,
                   credit_tree=True, layout=None):
    (fmt, line, rule) = make_summary_format(layout,
                                            max([tree.depth() for tree in trees]))
    header(fmt, rule, report_name, activity_name)
    tree_summary_lines(trees, 0, fmt, line, zeros, credit_tree)
    footer(rule)
