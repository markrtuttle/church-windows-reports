#!/usr/bin/env python

import report_style

def accounts_report(period_name, names,
                    chart, journal, budget, balance,
                    date_start, date_end, width=80, show_children=True):

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches

    if not names:
        return

    numbers = account_numbers(names, chart)

    (budgeted, unbudgeted) = classify_accounts(numbers, budget)

    first = True

    if budgeted:
        if not first:
            print
        first = False

        report_style.display_budgeted_accounts(
            "General Fund", period_name, budgeted, chart, balance, budget,
            width=width)

    if unbudgeted:
        if not first:
            print
        first = False

        report_style.display_accounts(
            "Other Funds", period_name, unbudgeted, chart, balance,
            width=width)

    numbers = budgeted + unbudgeted
    if show_children:
        def descendants(number):
            tree = [number]
            for num in chart.account(number).children():
                tree.extend(descendants(num))
            return tree
        for number in budgeted + unbudgeted:
            numbers.extend(descendants(number))

    entries = [entry for entry in journal.entries() if
               entry.number() in numbers
               and
               entry.date_is(date_start, date_end)]

    if entries:
        group = {}
        for entry in entries:
            name = entry.name()
            if group.get(name) is None:
                group[name] = []
            group[name].append(entry)

        for name in sorted(group.keys()):
            if not first:
                print
            first = False

            report_style.display_entries(
                group[name], chart,
                sort_keys=['date', 'reverse_amount'],
                width=width)

def account_numbers(names, chart):

    special_names = []
    account_names = []
    for name in names:
        if name in ['assets', 'checking', 'liabilities', 'vendors',
                    'funds', 'general']:
            special_names.append(name)
        else:
            account_names.append(name)

    account_names = [name.lower() for name in account_names]
    numbers = [num for num in chart.accounts()
               if chart.account(num).name().lower() in account_names]

    for name in special_names:
        if name == 'assets':
            numbers += [num for num in chart.accounts()
                        if chart.account(num).is_asset()
                        and chart.account(num).name() !=
                        'Cambridge Savings Bank Checking']

        if name == 'checking':
            numbers += [chart.number('Cambridge Savings Bank Checking')]

        if name == 'liabilities':
            numbers += [num for num in chart.accounts()
                        if chart.account(num).is_liability()
                        and num != chart.vendor_number()]

        if name == 'vendors':
            numbers += [chart.vendor_number()]

        if name == 'funds':
            numbers += [num for num in chart.accounts()
                        if chart.account(num).is_fund()
                        and chart.account(num).name() != 'General Fund'
                        and chart.account(num).parent() is None]

        if name == 'general':
            number = chart.number('General Fund')
            numbers += [number] + chart.account(number).children()

    return numbers

################################################################

def classify_accounts(numbers, budget):

    budgeted = []
    unbudgeted = []
    for number in numbers:
        if budget.balance(number) is not None:
            budgeted.append(number)
        else:
            unbudgeted.append(number)
    return (budgeted, unbudgeted)
