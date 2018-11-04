#!/usr/bin/env python

import amountt
import datet
from utility import truncate

def horizontal_line(width):
    print '-' * width

################################################################

def fund_report(report_name, period_name, numbers, chart, balance,
                width=80,
                name_w=25,
                amount_w=8,
                balance_w=10,
                name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    format_string = "| {:<{nw}} | {:>{aw}} | {:>{bw}} |"
    format_length = 2 + name_w + 3 + amount_w + 3 + balance_w + 2

    remaining_width = width - format_length
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad

    numbers.sort(key=lambda num: chart.account(num).name())

    width = 2 + name_w + 3 + amount_w + 3 + balance_w + 2
    horizontal_line(width)
    print format_string.format(
        "",
        truncate(period_name, amount_w),
        truncate("Current", balance_w),
        nw=name_w,
        aw=amount_w,
        bw=balance_w)
    print format_string.format(
        truncate(report_name, name_w),
        truncate("change", amount_w),
        truncate("balance", balance_w),
        nw=name_w,
        aw=amount_w,
        bw=balance_w)

    horizontal_line(width)

    for num in numbers:
        name = chart.account(num).name()
        activity = balance['activity'][num]
        current = balance['current'][num]
        if not activity and not current:
            continue
        print format_string.format(
            truncate(name, name_w),
            truncate(amountt.to_string(activity), amount_w),
            truncate(amountt.to_string(current), balance_w),
            nw=name_w,
            aw=amount_w,
            bw=balance_w)

    horizontal_line(width)

################################################################

def account_report(report_name, period_name, numbers, chart, balance, budget,
                   width=80,
                   name_w=21,
                   amount_w=8,
                   balance_w=10,
                   name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    format_string = ("| {:<{nw}} | {:>{aw}} "
                     "| {:>{bw}} {:>{bw}} {:>{bw}} {:>{aw}} |")
    format_length = (2 + name_w + 3 + amount_w + 3 +
                     3*(balance_w + 1) + amount_w + 2)

    remaining_width = width - format_length
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad

    width = (2 + name_w + 3 + amount_w + 3 + 3*(balance_w + 1) + amount_w + 2)

    if not numbers:
        return

    horizontal_line(width)
    print format_string.format(
        "",
        truncate(period_name, amount_w),
        truncate("Budget", balance_w),
        truncate("Budget", balance_w),
        truncate("Budget", balance_w),
        truncate("Percent", amount_w),
        nw=name_w,
        bw=balance_w,
        aw=amount_w)
    print format_string.format(
        truncate(report_name, name_w),
        truncate("expenses", amount_w),
        truncate("total", balance_w),
        truncate("spent", balance_w),
        truncate("left", balance_w),
        truncate("left", amount_w),
        nw=name_w,
        bw=balance_w,
        aw=amount_w)

    horizontal_line(width)

    for number in numbers:
        name = chart.account(number).name()
        activity = balance['activity'][number]
        total = budget.balance(number) if budget else None
        spent = balance['current'][number]
        if not activity and not total and not spent:
            continue
        remaining = total - spent
        try:
            percent_remaining = float(remaining) / float(total)
        except ZeroDivisionError:
            percent_remaining = 0
        percent_remaining = "{:.2f}".format(percent_remaining)
        print format_string.format(
            truncate(name, name_w),
            truncate(amountt.to_string(activity), amount_w),
            truncate(amountt.to_string(total), balance_w),
            truncate(amountt.to_string(spent), balance_w),
            truncate(amountt.to_string(remaining), balance_w),
            truncate(percent_remaining, amount_w),
            nw=name_w,
            bw=balance_w,
            aw=amount_w)

    horizontal_line(width)

################################################################

def transaction_report(name, journal, chart, ministry,
                       date_start, date_end, posted_start, posted_end,
                       width=80,
                       comment_w=35,
                       name_w=25,
                       amount_w=8,
                       name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    remaining_width = width - (name_w + 1 + amount_w + 1 + 5 + 1 + comment_w)
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width / 10 * 4
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    comment_w += remaining_width - name_pad

    numbers = ministry.accounts(name) + ministry.funds_accounts(name)
    entries = [entry for entry in journal.entries()
               if
               entry.number_is(numbers)
               and
               (entry.date_is(date_start, date_end)
                or
                (entry.posted_is(posted_start, posted_end)
                 and
                 entry.date_is(None, posted_end)))]
    entries.sort(key=lambda entry: (entry.name(), entry.date()))

    for entry in entries:
        (month, day, _) = datet.parse_ymd_string(entry.date())

        amount = (entry.debit() or 0) - (entry.credit() or 0)
        if chart.account(entry.number()).is_credit_account():
            amount = -amount


        print ("{3:<{nw}} {4:>{aw}} {0:>2}/{1:>2} {2:<{cw}}"
               .format(month, day,
                       truncate(entry.comment(), comment_w),
                       truncate(entry.name(), name_w),
                       truncate(amountt.to_string(amount), amount_w),
                       cw=comment_w,
                       nw=name_w,
                       aw=amount_w))

################################################################
