#!/usr/bin/env python

import amountt
import datet
from utility import truncate

def horizontal_line(width):
    print '-' * width

################################################################

def display_accounts(
        report_name, period_name, numbers, chart, balance,
        width=80,
        name_w=25,
        amount_w=8,
        balance_w=10,
        name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    format_string = "| {:<{nw}} | {:>{aw}} | {:>{bw}} |"
    format_length = lambda: 2 + name_w + 3 + amount_w + 3 + balance_w + 2

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    width = format_length()

    if not numbers:
        return
    numbers.sort(key=lambda num: chart.account(num).name())

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

def display_budgeted_accounts(
        report_name, period_name, numbers, chart, balance, budget,
        width=80,
        name_w=21,
        amount_w=8,
        balance_w=10,
        name_max=40):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    format_string = ("| {:<{nw}} | {:>{aw}} "
                     "| {:>{bw}} {:>{bw}} {:>{bw}} {:>{aw}} |")
    format_length = lambda: (2 + name_w + 3 + amount_w + 3 +
                             3*(balance_w + 1) + amount_w + 2)

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    width = format_length()

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

def display_entries(entries, chart,
                    group_by_month=False,
                    sort_keys=None,
                    width=80,
                    comment_w=35,
                    name_w=25,
                    amount_w=8,
                    name_max=40):

    # pylint: disable=too-many-arguments

    if not entries:
        return

    if sort_keys is None:
        sort_keys = ["date"]

    if group_by_month:
        group = group_entries_by_month(entries)
        group = sort_grouped_entries(group, sort_keys)

        first = True
        for month in sorted(group.keys(), reverse=True):
            month_entries = group[month]
            if not month_entries:
                continue
            if not first:
                print
            first = False
            print_entries(month_entries, chart,
                          width, comment_w, name_w, amount_w, name_max)
    else:
        entries = sort_entries(entries, sort_keys)
        print_entries(entries, chart,
                      width, comment_w, name_w, amount_w, name_max)

def sort_entries(entries, sort_keys):
    sort_keys.reverse()  # assume sort is stable
    for key in sort_keys:
        if key == "amount":
            entries.sort(key=lambda ent: ent.debit() or ent.credit())
            continue
        if key == "reverse_amount":
            entries.sort(key=lambda ent: ent.debit() or ent.credit(),
                         reverse=True)
            continue
        if key == "date":
            entries.sort(key=lambda ent: ent.date())
            continue
        if key == "reverse_date":
            entries.sort(key=lambda ent: ent.date(), reverse=True)
            continue
        if key == "name":
            entries.sort(key=lambda ent: ent.name())
            continue
        if key == "comment":
            entries.sort(key=lambda ent: ent.comment())
            continue
        raise ValueError("Can't sort entries by {}".format(key))
    return entries

def group_entries_by_month(entries):
    group = {mon: [] for mon in range(1, 13)}
    for entry in entries:
        (month, _, _) = datet.parse_ymd_string(entry.date())
        group[month].append(entry)
    return group

def sort_grouped_entries(groups, sort_keys):
    sorted_groups = {}
    for index in groups:
        sorted_groups[index] = sort_entries(groups[index], sort_keys)
    return sorted_groups

def print_entries(entries, chart,
                  width, comment_w, name_w, amount_w, name_max):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    format_string = "{:>{aw}} {:>2}/{:>2} {:<{nw}} {:<{cw}}"
    format_length = lambda: amount_w + 1 + 5 + 1 + name_w + 1 + comment_w

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width / 10 * 4
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    comment_w += remaining_width - name_pad

    for entry in entries:
        (month, day, _) = datet.parse_ymd_string(entry.date())

        amount = (entry.debit() or 0) - (entry.credit() or 0)
        if chart.account(entry.number()).is_credit_account():
            amount = -amount

        print (format_string
               .format(truncate(amountt.to_string(amount), amount_w),
                       month, day,
                       truncate(entry.name(), name_w),
                       truncate(entry.comment(), comment_w),
                       cw=comment_w,
                       nw=name_w,
                       aw=amount_w))

################################################################
