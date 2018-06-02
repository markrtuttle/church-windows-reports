#!/usr/bin/env python

# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments

import amount
import date
import entry

################################################################

def join_nonempty(sep, strings):
    strings = [string for string in strings if string != ""]
    return sep.join(strings)

def truncate(string, length=None):
    if length is None:
        return string
    if len(string) <= length:
        return string
    return string[:(length-3)]+"..."

def split_width(width, lratio=.4, lmin=None, lmax=None, rmin=None, rmax=None):
    lmin = lmin or 0
    lmax = lmax or width
    rmin = rmin or 0
    rmax = rmax or width

    if lmin + rmin > width:
        raise ValueError("lmin + rmin > width")
    if lmin > lmax:
        raise ValueError("lmin > lmax")
    if rmin > rmax:
        raise ValueError("rmin > rmax")
    if lratio > 1:
        raise ValueError("lratio > 1")

    left = int(width * lratio)
    left = max(lmin, left)
    left = min(lmax, left)

    right = width - left
    right = max(rmin, right)
    right = min(rmax, right)

    if left + right != width:
        raise ValueError("left + right != width")

    return (left, right)

def format_string(width, right=False):
    if right:
        return '{:>' + str(width) + '}'
    return '{:' + str(width) + '}'

################################################################

def income_statement(numbers, income, title, month, year,
                     sort_names=True, zeros=False):

    lines = income.accounts(numbers)
    if not lines:
        return

    if sort_names:
        lines.sort(key=lambda ent: ent.name())

    print ""
    if title:
        print title

    print ("{:<42} {:>10} {:>10} {:>10}"
           .format("", month, year, "Budget"))
    for line in lines:
        # pylint: disable=bad-continuation
        if (not zeros and
            amount.eq(line.month(), "0") and
            amount.eq(line.ytd(), "0") and
            line.budget() is None):
            continue
        print ("  {:<40} {:>10} {:>10} {:>10}"
               .format(truncate(line.name(), 40),
                       line.month(),
                       line.ytd(),
                       line.budget()))

def balance_statement(numbers, balance, title, month,
                      sort_names=True, zeros=False):

    lines = balance.accounts(numbers)
    if not lines:
        return

    if sort_names:
        lines.sort(key=lambda ent: ent.name())

    print ""
    if title:
        print title

    print "{:<42} {:>10} {:>10}".format("", month, "Balance")
    for line in lines:
        # pylint: disable=bad-continuation
        if (not zeros and
            amount.eq(line.month(), "0") and
            amount.eq(line.ytd(), "0")):
            continue
        print ("  {:<40} {:>10} {:>10}"
               .format(truncate(line.name(), 40),
                       line.month(),
                       line.ytd()))


def journal_statement(numbers, journal, width, title,
                      entries=None, compress=False,
                      is_debit_account=None):
    # pylint: disable=too-many-locals
    if numbers is not None:
        my_number = lambda number: number in numbers
        entries = journal.number_is(my_number, entries)
    if not entries:
        return

    entries = sort_by_account_within_date(entries)

    if title:
        print "\n"+title

    if compress:
        wid = width - (10 + 1 + 5 + 1 + 1)
        fmt = "{:>10} {:5} {:" + str(wid) + "}"
        print "\n"+fmt.format("Amount", "Date", "Description")
        for ent in entries:
            if ent is None:
                print
                continue
            dat = date.fmt(ent.date(), False)
            amt = amount.fmt(ent.debit() or ent.credit(),
                             is_debit_account=is_debit_account,
                             is_debit_entry=ent.is_debit(),
                             postfix=True)
            desc = join_nonempty(":  ", [ent.name(), ent.comment()])
            desc = desc.replace("Income", "Inc")
            desc = desc.replace("Expense", "Exp")
            desc = desc.replace("Maintenance", "Maint")
            print (fmt.format(amt,
                              dat,
                              truncate(desc, wid)))
    else:
        (lwid, rwid) = split_width(width - (10 + 1 + 5 + 1 + 1))
        lfmt = format_string(lwid)
        rfmt = format_string(rwid)
        fmt = "{:>10} {:5} " + lfmt + " " + rfmt
        print "\n"+fmt.format("Amount", "Date", "Account", "Comment")
        for ent in entries:
            if ent is None:
                print
                continue
            dat = date.fmt(ent.date(), False)
            amt = amount.fmt(ent.debit() or ent.credit(),
                             is_debit_account=is_debit_account,
                             is_debit_entry=ent.is_debit(),
                             postfix=True)
            print (fmt.format(amt,
                              dat,
                              truncate(ent.name(), lwid),
                              truncate(ent.comment(), rwid)))

def subaccount_balance_statement(chart, balance, month, year, parent_name,
                                 sort_names=True, zeros=False):
    # pylint: disable=bad-continuation
    # pylint: disable=too-many-locals
    parent_number = chart.number(parent_name)
    child_numbers = chart.account(parent_number).children()
    if sort_names:
        child_numbers.sort(key=lambda num: chart.account(num).name())
    lines = []
    for num in child_numbers:
        bal = balance.account(num)
        if (not zeros and
            amount.eq(bal.month(), "0") and
            amount.eq(bal.ytd(), "0")):
            continue
        lines.append((bal.name(), bal.month(), bal.ytd()))
    if not lines:
        return
    fmt = "{:40} {:>10} {:>10}"
    print
    print fmt.format(parent_name, month, year)
    print
    lines.sort(key=lambda tup: tup[0])
    for name_, month_, year_ in lines:
        print fmt.format("  "+name_, month_, year_)

def trailer(date_start, date_end, posted_start):
    print ("\nTransactions shown are those occurring between {} and {}, "
           "\nand those occuring before {} but posted after {}"
           .format(date_start, date_end, date_start, posted_start))

################################################################

def sort_by_account_within_date(entries,
                                account_reverse=False,
                                date_reverse=True,
                                insert_none=True):

    months = range(1, 13) if not date_reverse else range(12, 0, -1)

    bucket = {month: [] for month in months}
    for ety in entries:
        (month, _, _) = date.parse(ety.date())
        bucket[month].append(ety)

    for month in months:
        bucket[month].sort(key=entry.date_key)
        bucket[month].sort(key=entry.account_key, reverse=account_reverse)

    new_entries = []
    first_month = True
    for month in months:
        if not bucket[month]:
            continue
        if not first_month and insert_none:
            new_entries.extend([None])
        first_month = False
        new_entries.extend(bucket[month])
    return new_entries

################################################################
