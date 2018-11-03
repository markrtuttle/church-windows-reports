#!/usr/bin/env python

import amountt
from utility import truncate


def display_subfunds(name, chart, balance,
                     width, name_w, amount_w, balance_w, name_max):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    remaining_width = width - (2 + name_w + 1 + amount_w + 1 + balance_w)
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad

    number = chart.number(name)
    numbers = chart.account(number).children()
    numbers.sort(key=lambda num: chart.account(num).name())

    print ("{:<{nw}}   {:>{aw}} {:>{bw}}"
           .format(truncate(name, name_w),
                   truncate("Month", amount_w),
                   truncate("Balance", balance_w),
                   nw=name_w,
                   aw=amount_w,
                   bw=balance_w))

    activity_ = balance['activity']
    current_ = balance['current']
    for num in numbers:
        account = chart.account(num)
        activity = activity_[num]
        current = current_[num]
        if not activity and not current:
            continue
        print ("  {:<{nw}} {:>{aw}} {:>{bw}}"
               .format(truncate(account.name(), name_w),
                       truncate(amountt.to_string(activity), amount_w),
                       truncate(amountt.to_string(current), balance_w),
                       nw=name_w,
                       aw=amount_w,
                       bw=balance_w))

def subfund_report(chart, balance,
                   width=80,
                   name_w=25,
                   amount_w=8,
                   balance_w=10,
                   name_max=40):

    # pylint: disable=too-many-arguments

    display_subfunds("Special Funds", chart, balance,
                     width, name_w, amount_w, balance_w, name_max)

    print

    display_subfunds("Investment Return", chart, balance,
                     width, name_w, amount_w, balance_w, name_max)
