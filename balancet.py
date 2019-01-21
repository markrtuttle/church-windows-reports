

def accumulate_children(number, chart, balance):
    children = chart.account(number).children()
    if not children:
        return balance

    total = 0
    kind = chart.account(number).is_debit_account()
    for num in children:
        balance = accumulate_children(num, chart, balance)
        num_kind = chart.account(num).is_debit_account()
        total += balance.get(num, 0) * (1 if kind == num_kind else -1)
    balance[number] += total
    return balance

def balances(chart, journal, initial, start=None, end=None):

    # pylint: disable=too-many-locals

    prior_credit = {}
    prior_debit = {}
    period_credit = {}
    period_debit = {}
    for entry in journal.entries():
        num = entry.number()
        debit = entry.debit() or 0
        credit = entry.credit() or 0
        if entry.date_is(None, start) and entry.date() != start:
            prior_debit[num] = prior_debit.get(num, 0) + debit
            prior_credit[num] = prior_credit.get(num, 0) + credit
            continue
        if entry.date_is(start, end):
            period_debit[num] = period_debit.get(num, 0) + debit
            period_credit[num] = period_credit.get(num, 0) + credit
            continue

    prior_balance = {}
    current_balance = {}
    activity = {}
    for num in chart.accounts():
        prior_balance[num] = initial.balance(num)
        current_balance[num] = initial.balance(num)

        prior_change = prior_debit.get(num, 0) - prior_credit.get(num, 0)
        period_change = period_debit.get(num, 0) - period_credit.get(num, 0)
        if chart.account(num).is_credit_account():
            prior_change = -prior_change
            period_change = -period_change

        prior_balance[num] += prior_change
        current_balance[num] += prior_change + period_change
        activity[num] = period_change

    for num in prior_balance:
        if chart.account(num).parent() is None:
            prior_balance = accumulate_children(num, chart, prior_balance)
            current_balance = accumulate_children(num, chart, current_balance)
            activity = accumulate_children(num, chart, activity)

    return {'prior': prior_balance,
            'current': current_balance,
            'activity': activity}
