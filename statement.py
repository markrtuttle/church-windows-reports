#!/usr/bin/env python

# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments

# TODO: trailer should use date_end from journal.csv as of date

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

def income_statement(numbers, income, title, month,
                     sort_names=True, zeros=False):

    lines = income.accounts(numbers)
    if not lines:
        print "\n  Nothing to report."
        return False

    if sort_names:
        lines.sort(key=lambda ent: ent.name())

    print ""
    if title:
        print title

    print_income_hbar()
    print_income_header(month)
    print_income_hbar()
    for line in lines:
        # pylint: disable=bad-continuation
        if (not zeros and
            amount.eq(line.month(), "0") and
            amount.eq(line.ytd(), "0") and
            line.budget() is None):
            continue
        print_income_entry(truncate(line.name(), 40),
                            line.month(),
                            line.budget(),
                            line.ytd())
    print_income_hbar()

    return True

def balance_statement(numbers, balance, title, month,
                      sort_names=True, zeros=False):

    lines = balance.accounts(numbers)
    if not lines:
        print "\n  Nothing to report."
        return False

    if sort_names:
        lines.sort(key=lambda ent: ent.name())

    print ""
    if title:
        print title

    print_balance_hbar()
    print_balance_header(month)
    print_balance_hbar()
    for line in lines:
        # pylint: disable=bad-continuation
        if (not zeros and
            amount.eq(line.month(), "0") and
            amount.eq(line.ytd(), "0")):
            continue
        print_balance_line(truncate(line.name(), 40),
                           line.month(),
                           line.ytd())
    print_balance_hbar()

    return True

def journal_statement(numbers, journal, width, title,
                      entries=None, compress=False,
                      is_debit_account=None,
                      amount_sort=False):
    # pylint: disable=too-many-locals
    if numbers is not None:
        my_number = lambda number: number in numbers
        entries = journal.number_is(my_number, entries)

    if not entries:
        print "\n  No activity to report."
        return

    entries = sort_by_account_within_date(entries, amount_sort=amount_sort)

    if title:
        print "\n"+title

    if compress:
        wid = width - (10 + 1 + 5 + 1 + 1)
        fmt = "{:>10} {:5} {:" + str(wid) + "}"
        print "\n"+fmt.format("Amount", "Date", "Description")+"\n"
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
        print "\n"+fmt.format("Amount", "Date", "Account", "Comment")+"\n"
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
                                insert_none=True,
                                amount_sort=False):

    months = range(1, 13) if not date_reverse else range(12, 0, -1)

    bucket = {month: [] for month in months}
    for ety in entries:
        (month, _, _) = date.parse(ety.date())
        bucket[month].append(ety)

    for month in months:
        bucket[month].sort(key=entry.date_key)
        bucket[month].sort(key=entry.account_key, reverse=account_reverse)
        if amount_sort:
            bucket[month].sort(key=entry.amount_key, reverse=True)

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

def print_hbar(width=80, indent=0):
    width = width - indent
    print "{:>{ind}}{:->{wid}}".format("", "", ind=indent, wid=width)

################################################################

INCOME_FMT = "{sp:<{id}}| {:<{nw}} | {:>{aw}} | {:>{aw}} {:>{aw}} {:>{aw}} {:>{pw}} |"
def print_income_line(name, month_spent,
                      year_budget, year_spent, year_left, year_percent,
                      indent=2, namew=40, amountw=10, percentw=10,
                      fmt=INCOME_FMT):
    print (fmt.format(name, month_spent,
                      year_budget, year_spent, year_left, year_percent,
                      sp="",
                      id=indent, nw=namew, aw=amountw, pw=percentw))

def print_income_hbar():
    print_hbar(width=105, indent=2)

def print_income_header(month, indent=2, namew=40, amountw=10, percentw=10):
    print_income_line("", month,
                      "Budget", "Budget", "Budget", "Percent",
                      indent=indent,
                      namew=namew, amountw=amountw, percentw=percentw)
    print_income_line("General fund expense accounts", "expenses",
                      "total", "spent", "left", "left",
                      indent=indent,
                      namew=namew, amountw=amountw, percentw=percentw)

def print_income_entry(name, month_spent, year_budget, year_spent):
    year_left = amount.cents(year_budget) - amount.cents(year_spent)
    try:
        year_percent = float(year_left) / amount.cents(year_budget)
    except ZeroDivisionError:
        year_percent = 0
    year_percent = "{:.2f}".format(year_percent)
    print_income_line(name, month_spent,
                      year_budget, year_spent,
                      amount.cents_fmt(year_left),
                      year_percent)

################################################################

BALANCE_FMT = "{sp:<{id}}| {:<{nw}} | {:>{aw}} {:>{aw}} |"
def print_balance_line(name, month_spent, year_spent,
                       indent=2, namew=40, amountw=10,
                       fmt=BALANCE_FMT):
    print (fmt.format(name, month_spent, year_spent,
                      sp="", id=indent, nw=namew, aw=amountw))

def print_balance_hbar():
    print_hbar(width=70, indent=2)

def print_balance_header(month, indent=2, namew=40, amountw=10):
    print_balance_line("", month, "Current",
                       indent=indent, namew=namew, amountw=amountw)
    print_balance_line("Fund name", "change", "balance",
                       indent=indent, namew=namew, amountw=amountw)

def print_balance_entry(name, month_spent, year_spent):
    print_balance_line(name, month_spent, year_spent)
