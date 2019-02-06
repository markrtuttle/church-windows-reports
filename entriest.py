import amountt
import entryt
import accountt

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

def select_by_amount(entries, low=None, high=None):
    low = amountt.from_string(low)
    high = amountt.from_string(high)
    def select(amount):
        if amount is None:
            return None
        amt = abs(amount)
        return ((low is None or low <= amt)
                and
                (high is None or amt <= high))

    return [entry for entry in entries
            if select(entry.credit() or entry.debit())]

def select_debit(entries):
    return [entry for entry in entries
            if accountt.is_debit_number(entry.number())]

def select_bill(entries):
    return [entry for entry in entries if entry.type() == entryt.BILL]

def sort_by_date(entries, reverse=False):
    key = lambda entry: entry.date()
    return sorted(entries, key=key, reverse=reverse)

def sort_by_name(entries, reverse=False):
    key = lambda entry: entry.name()
    return sorted(entries, key=key, reverse=reverse)

def sort_by_amount(entries, reverse=False):
    key = lambda entry: abs(entry.debit() or entry.credit())
    return sorted(entries, key=key, reverse=reverse)

def group_by_month(entries, reverse=False):
    group = {}
    for entry in entries:
        date = entry.date()[:7] # grab yyyy/mm from yyyy/mm/dd
        group[date] = group.get(date, []) + [entry]
    return [group[date] for date in sorted(group, reverse=reverse)]
