#!/usr/bin/env python

import treet
import amountt
import accountt

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

    def format_line(name, activity, balance, level=0):
        name = " "*(2*level) + name
        name = name[:name_w]
        act = activity + " "*(2*level)
        bal = balance  + " "*(2*level)
        print string.format(name, act, bal)

    def print_line(name, activity, balance, level=0):
        format_line(name, amountt.to_string(activity), amountt.to_string(balance), level)

    def print_rule():
        print '-'*width

    return (format_line, print_line, print_rule)

def tree_summary_line(tree, chart, balance, level, print_line, zeros, credit_tree):

    (number, trees) = tree

    name = chart.account(number).name()
    activity = balance.activity(number)
    current = balance.current(number)

    if credit_tree != accountt.is_credit_number(number):
        activity = -activity
        current = -current

    if zeros or activity or current:
        print_line(name, activity, current, level)
    tree_summary_lines(trees, chart, balance, level+1, print_line, zeros, credit_tree)

def tree_summary_lines(trees, chart, balance, level, print_line, zeros, credit_tree):
    for tree in trees:
        tree_summary_line(tree, chart, balance, level, print_line, zeros, credit_tree)

def header(line, rule, report_name=None, activity_name=None, balance_name=None):
    rule()
    line("", activity_name, balance_name)
    line(report_name, "activity", "balance")
    rule()

def footer(rule):
    rule()

def tree_summary(tree, chart, balance, report_name=None, activity_name=None, balance_name=None, zeros=True,
                 credit_tree=True):
    (fmt, line, rule) = make_summary_format(level_max=treet.depth(tree))
    header(fmt, rule, report_name, activity_name, balance_name)
    tree_summary_line(tree, chart, balance, 0, line, zeros=zeros, credit_tree=credit_tree)
    footer(rule)

def tree_summaries(trees, chart, balance, report_name=None, activity_name=None, balance_name=None, zeros=True,
                   credit_tree=True):
    (fmt, line, rule) = make_summary_format(level_max=max([treet.depth(tree) for tree in trees]))
    header(fmt, rule, report_name, activity_name, balance_name)
    tree_summary_lines(trees, chart, balance, 0, line, zeros=zeros, credit_tree=credit_tree)
    footer(rule)
