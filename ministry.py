#!/usr/bin/env python

# pylint: disable=missing-docstring

import json

import number
import balance
import chart

# TODO: Make a ministry json file for input

################################################################

ACCOUNTS = {
    "outreach": {
        "name": "Outreach",
        "budget": [
            "Outreach Fund Contribution",
        ],
        "fund": [
            "Adopt a Family",
            "Adopt a Vet",
            "Arlington Food Pantry Fund",
            "Housing Corp. of Arlington",
            "Neighbors In Need",
            "One Great Hour of Sharing",
            "Outreach Fund",
            "Relief Fund",
            "UCC Christmas Fund",
        ]
    },
    "property": {
        "name": "Property",
        "budget": [
            "Church Grounds",
            "Church Maintenance",
            "Custodial Service",
            "Custodial Supplies",
            "Electric",
            "Emergency Property Fund Contribution",
            "Gas",
            "Oil",
            "Parsonage Electric",
            "Parsonage Grounds",
            "Parsonage Maintenance",
            "Parsonage Oil",
            "Parsonage Water/Sewer",
            "Telephone",
            "Water/Sewer",
        ],
        "fund": [
            "Emergency Property Fund",
        ]
    },
    "education": {
        "name": "Christian Education",
        "budget": [
            "Christian Education",
        ],
        "fund": [
            "Youth Fund",
        ]
    },
    "stewardship": {
        "name": "Stewardship",
        "budget": [
        ],
        "fund": [
            "Environmental Stewardship",
        ]
    },
    "worship": {
        "name": "Worship",
        "budget": [
            "Additional Pastor Related Expenses",
            "Pulpit Supply",
            "Worship",
        ],
        "fund": [
            "Flower Fund",
        ]
    },
    "finance": {
        "name": "Finance",
        "budget": [
            ],
        "fund": [
            "Capital Campaign 2009 Return",
            "Crockett Memorial Return",
            "Hayes Memorial Return",
            "Jackson Legacy Return",
            "Jennings Memorial Return",
            "Legacy Return",
            "Memorial Return",
            "PSCC Legacy Return",
            "Skinner/Hall Memorial Return",
            "Smith Memorial Return",
        ],
    },
    "administration": {
        "name": "Administration",
        "budget": [
            "Additional Property & Search Expenses",
            "Association Dues",
            "Bank Service Charges",
            "Interchurch",
            "Office Expense",
            "Parsonage Basic Telephone",
            "Pastoral Discretionary Expenses",
            "Pastor's Auto Allowance",
            "Pastor's Books/Cont Ed Expense",
            "Pastor's Furnishings",
            "Payroll Services",
            "Property/Liability Insurance",
            "Social Media / Communications",
            "Workers Comp. Insurance",
        ],
        "fund": [
            "Special Event",
            "Women's Guild",
        ]
    },
    "membership": {
        "name": "Membership",
        "budget": [
            "Membership",
        ],
        "fund": [
        ]
    },
    "music": {
        "name": "Music",
        "budget": [
            "Music",
        ],
        "fund": [
            "Music Fund",
            "Organ Restoration",
        ]
    },
    "hospitality": {
        "name": "Hospitality",
        "budget": [
        ],
        "fund": [
            "Hospitality Fund",
        ]
    }
}

################################################################

class Ministry(object):
    def __init__(self, coa):
        self.accounts_ = ACCOUNTS
        self.coa_ = coa
        self.unassigned = self.unused_names()
        if not self.validate():
            raise ValueError("Inconsistent ministry assignments")

    def keys(self):
        result = [key_ for key_ in self.accounts_
                  if not key_.startswith("ignore")]
        result.sort()
        return result

    def keys_unassigned(self):
        result = [key_ for key_ in self.accounts_
                  if key_.startswith("ignore")]
        result.sort()
        return result

    def name(self, ministry_name):
        return self.accounts_[ministry_name]["name"]

    def accounts(self, ministry_name):
        return [self.coa_.number(name_)
                for name_ in self.accounts_[ministry_name]["budget"]]

    def funds(self, ministry_name):
        return [self.coa_.number(name_)
                for name_ in self.accounts_[ministry_name]["fund"]]

    def fund_accounts(self, fund_number):
        fund_account = self.coa_.account(fund_number)
        return fund_account.income() + fund_account.expense()

    def funds_accounts(self, ministry_name):
        result = []
        for fund_number in self.funds(ministry_name):
            result.extend(self.fund_accounts(fund_number))
        return result

    def unassigned_names(self, kind):
        # kind is budget, asset, fund, liability
        try:
            return self.unassigned[kind]
        except KeyError:
            raise ValueError("Unknown kind '{}' of unassigned account".
                             format(kind))

    def dump_jsons(self):
        return json.dumps(self.accounts_, indent=2)

################################################################

    def validate(self):
        for key in self.accounts_:
            for kind in ["budget", "fund"]:
                for name in self.accounts_[key][kind]:
                    try:
                        self.coa_.number(name)
                    except KeyError:
                        raise ValueError("Ministry account '{}' not in chart"
                                         .format(name))
        return True

################################################################

    def used_accounts(self):
        def numbers(names):
            return [self.coa_.number(name) for name in names]
        used = {}
        used["budget"] = []
        used["asset"] = []
        used["liability"] = []
        used["fund"] = []
        for key in self.keys():
            used["budget"] += numbers(self.accounts_[key]["budget"])
            used["fund"] += numbers(self.accounts_[key]["fund"])
        return used

    def chart_accounts(self):
        cht = {}
        cht["budget"] = []
        cht["asset"] = []
        cht["liability"] = []
        cht["fund"] = []
        general_fund = self.coa_.number("General Fund")
        for num in self.coa_.account_:
            act = self.coa_.account(num)
            if act.is_asset():
                cht["asset"].append(num)
                continue
            if act.is_liability():
                cht["liability"].append(num)
                continue
            if act.is_fund():
                cht["fund"].append(num)
                continue
            # Account is an income or expense account
            if number.eq(act.parent(), general_fund):
                cht["budget"].append(num)
        return cht

    def unused_accounts(self):
        used = self.used_accounts()
        cht = self.chart_accounts()
        general_fund = self.coa_.number("General Fund")
        unused = {}
        unused["budget"] = diff_number_list(cht["budget"], used["budget"])
        unused["asset"] = diff_number_list(cht["asset"], used["asset"])
        unused["fund"] = diff_number_list(cht["fund"],
                                          used["fund"] + [general_fund])
        unused["liability"] = diff_number_list(cht["liability"],
                                               used["liability"])
        return unused

    def unused_names(self):
        accounts = self.unused_accounts()
        from pprint import pprint
        pprint(accounts)
        def names(numbers):
            return [self.coa_.account(num).name() for num in numbers]
        unused = {}
        unused["budget"] = names(accounts["budget"])
        unused["asset"] = names(accounts["asset"])
        unused["fund"] = names(accounts["fund"])
        unused["liability"] = names(accounts["liability"])
        return unused

def diff_number_list(lista, listb):
    lista.sort(key=number.key)
    listb.sort(key=number.key)
    diff = []
    while lista and listb:
        heada = lista[0]
        headb = listb[0]
        compare = number.compare(heada, headb)
        if compare < 0:
            diff.append(heada)
            lista = lista[1:]
            continue
        if compare > 0:
            listb = listb[1:]
            continue
        lista = lista[1:]
        listb = listb[1:]
    return diff+lista


def main():
    bal = balance.Balance("balance.csv")
    cht = chart.Chart("chart.csv", bal)
    mty = Ministry(cht)
    unused = mty.unused_accounts()

    from pprint import pprint

    def names(numbers):
        return [cht.account(num).name() for num in numbers]
    display = {}
    for key in unused:
        display[key] = names(unused[key])
    pprint(display)


if __name__ == "__main__":
    main()
