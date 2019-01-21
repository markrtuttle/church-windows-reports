import treet

class Balance(object):

    def __init__(self, chart, entries, initial, start=None, end=None):

        def accumulate(number, chart, value):
            val = value[number]
            pvals = [value[child]
                     for child in chart.account(number).children() if
                     (chart.account(number).is_debit_account() ==
                      chart.account(child).is_debit_account())]
            nvals = [value[child]
                     for child in chart.account(number).children() if
                     (chart.account(number).is_debit_account() !=
                      chart.account(child).is_debit_account())]
            return val + sum(pvals) - sum(nvals)

        self.prior_ = {}
        self.current_ = {}
        prior_credit = {}
        prior_debit = {}
        current_credit = {}
        current_debit = {}
        for number in chart.accounts():
            self.prior_[number] = initial.balance(number)
            self.current_[number] = initial.balance(number)
            prior_credit[number] = 0
            prior_debit[number] = 0
            current_credit[number] = 0
            current_debit[number] = 0

        for entry in entries:
            number = entry.number()
            credit = entry.credit() or 0
            debit = entry.debit() or 0
            if entry.date_is(None, start) and entry.date() != start:
                prior_credit[number] += credit
                prior_debit[number] += debit
            if entry.date_is(start, end):
                current_credit[number] += credit
                current_debit[number] += debit

        for number in treet.walk_chart(chart):
            pchange = prior_debit[number] - prior_credit[number]
            cchange = current_debit[number] - current_credit[number]
            if chart.account(number).is_debit_account():
                self.prior_[number] += pchange
                self.current_[number] += pchange + cchange
            else:
                self.prior_[number] -= pchange
                self.current_[number] -= pchange + cchange

            self.prior_[number] = accumulate(number, chart, self.prior_)
            self.current_[number] = accumulate(number, chart, self.current_)

    def prior(self, number):
        return self.prior_[number]

    def current(self, number):
        return self.current_[number]

    def activity(self, number):
        return self.current(number) - self.prior(number)
