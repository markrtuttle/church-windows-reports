import amountt

def select_by_number(entries, numbers):
    return [entry for entry in entries if entry.number() in numbers]

def select_by_date(entries, date_start, date_end,
                   posted_start=None, posted_end=None):
    return [entry for entry in entries if
            entry.date_is(date_start, date_end)
            or
            (posted_start and posted_end
             and
             entry.posted_is(posted_start, posted_end)
             and
             entry.date_is(None, posted_end))]

def select_by_amount(entries, amt_min=None, amt_max=None):
    amt_min = amountt.from_string(amt_min)
    amt_max = amountt.from_string(amt_max)
    def select(amount):
        if amount is None:
            return None
        amt = abs(amountt.from_string(amount))
        return ((amt_min is None or amt_min <= amt)
                and
                (amt_max is None or amt <= amt_max))

    return [entry for entry in entries
            if select(entry.credit() or entry.debit())]

def sort_by_date(entries, reverse=False):
    key = lambda entry: entry.date()
    return sorted(entries, key=key, reverse=reverse)

def sort_by_name(entries, chart, reverse=False):
    key = lambda entry: chart.account(entry.number()).name()
    return sorted(entries, key=key, reverse=reverse)

def sort_by_amt(entries, reverse=False):
    key = lambda entry: abs(entry.debit() or entry.credit())
    return sorted(entries, key=key, reverse=reverse)

def group_by_month(entries, reverse=False):
    group = {}
    for entry in entries:
        date = entry.date()[:6] # grab yyyymm from yyyymmdd
        group[date] = group.get(date, []) + entry
    return [group[date] for date in sorted(group, reverse=reverse)]
