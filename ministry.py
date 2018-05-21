#!/usr/bin/env python

# pylint: disable=missing-docstring

import json

import number

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
    },
    "ignore": {
        "name": "Other",
        "asset": [
            "Cambridge Savings Bank Checking",
            "UCF Moderate Balanced Fund (Legacy)",
            "UCF Moderate Balanced Fund (Hayes)",
            "UCF Moderate Balanced Fund (Skinner/Hall)",
            "UCF Moderate Balanced Fund (Memorial)",
            "UCF Moderate Balanced Fund (PSCC)",
            "T Rowe Price Equity Income Fund (Jackson)",
            "Domini Social Equity Fund (Jennings)",
            "Cambridge Savings Bank CD (Smith)",
            "ManuLife (Capital Campaign 2009)",
            "Schwab One Account",
            "Cash",
        ],
        "liability": [
            "A Place to Grow Security Deposit",
            "Pastor Home Equity Liability",
        ],
        "fund": [
            "General Fund",
            "Special Funds",
            "Restricted Legacy Fund",
            "Investment Return",
            "Restricted Memorial Fund",
            "Capital Campaign 2009 Fund",
            "Capital Fund",
            "Crockett Memorial",
            "Hayes Memorial",
            "Jackson Legacy",
            "Jennings Memorial",
            "Legacy Fund",
            "Memorial Fund",
            "Parental Leave Fund",
            "Deacons Fund",
            "Departure Gift",
            "Designated Gift",
            "Prepaid Pledges",
            "PSCC Legacy Fund",
            "Roof Self-Loan",
            "Sabbatical Fund",
            "Sarah's Circle",
            "Skinner/Hall Memorial",
            "Smith Memorial",
        ],
        "income": [
            "A Place to Grow Income",
            "Christmas Envelope",
            "Church School",
            "Country Dance Society Income",
            "Easter Envelope",
            "Education Dir. FICA",
            "Education Dir. Salary",
            "Folk Arts Center Income",
            "Gift",
            "Holiday Fair Income",
        ],
        "expense": [
            "Home Equity/Compensation",
            "Initial Payment & Assoc. Dues",
            "Life and Disability Insurance",
            "Loose Collection",
            "Misc Income",
            "Miscellaneous Rental Income",
            "Office Personnel Compensation",
            "Office Personnel FICA",
            "Organist Compensation",
            "Organist FICA",
            "Other Fundraising Income",
            "Parental Leave Fund Contribution",
            "Pastor's Annuity",
            "Pastor's FICA Reimbursement",
            "Pastor's FSA expense",
            "Pastor's Health Insurance",
            "Pastor's Salary",
            "Philharmonic Society of Arlington Income",
            "Pledges",
            "Prior Year Payment",
            "Royal Scottish Dance Team Income",
            "Rummage Sale Income",
            "Sabbatical Fund Contribution",
            "Thanksgiving Envelope",
            "UCF Moderate Balanced Fund",
            "Vox Lucens/Jay Lane Income",
            "Youth Choir Dir Comp",
            "Youth Choir Dir FICA",
        ]
    }
}

################################################################

class Ministry(object):
    def __init__(self, coa):
        self.accounts_ = ACCOUNTS
        self.coa_ = coa
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

    def dump_jsons(self):
        return json.dumps(self.accounts_, indent=2)

################################################################

    def ministry_numbers(self):
        def insert(num, nums, warnings=True):
            if num in nums and warnings:
                print "Number {} assigned to two ministries".format(num)
            nums.add(num)
            return nums
        def insert_name(name, nums, warnings=True):
            num = self.coa_.number(name)
            return insert(num, nums, warnings)

        numbers = set()
        for name in self.keys():
            for num in self.accounts(name):
                numbers = insert(num, numbers)
            for num in self.funds(name):
                numbers = insert(num, numbers)
            for num in self.funds_accounts(name):
                numbers = insert(num, numbers)
        for name in self.keys_unassigned():
            act = self.accounts_[name]
            for name_ in act.get("asset", []):
                numbers = insert_name(name_, numbers)
            for name_ in act.get("liability", []):
                numbers = insert_name(name_, numbers)
            for name_ in act.get("income", []):
                numbers = insert_name(name_, numbers)
            for name_ in act.get("expense", []):
                numbers = insert_name(name_, numbers)
            for name_ in act.get("fund", []):
                numbers = insert_name(name_, numbers)
                num_ = self.coa_.number(name_)
                act = self.coa_.account(num_)
                for num in act.income() + act.expense():
                    numbers = insert(num, numbers, name_ != "General Fund")
        nums = list(numbers)
        nums.sort(key=number.key)
        return nums

    def chart_numbers(self):
        nums = list(self.coa_.account_.keys())
        nums.sort(key=number.key)
        return nums

    def validate(self):
        mnumbers = self.ministry_numbers()
        cnumbers = self.chart_numbers()
        equal = True
        while mnumbers and cnumbers:
            compare = number.compare(mnumbers[0], cnumbers[0])
            if compare == 0:
                mnumbers = mnumbers[1:]
                cnumbers = cnumbers[1:]
                continue
            if compare < 0:
                print "1 Ministry number {} not in chart".format(mnumbers[0])
                equal = False
                mnumbers = mnumbers[1:]
            else:
                print "2 Chart number {} not in ministry".format(cnumbers[0])
                equal = False
                cnumbers = cnumbers[1:]

        while mnumbers:
            print "3 Ministry number {} not in chart".format(mnumbers[0])
            equal = False
            mnumbers = mnumbers[1:]

        while cnumbers:
            print "4 Chart number {} not in ministry".format(cnumbers[0])
            equal = False
            cnumbers = cnumbers[1:]

        return equal

################################################################

ACCOUNTS1 = {
    "outreach": [
        "Adopt a Family", # 3.021.020.000
        "Adopt A Family Expense", # 5.520.002.000
        "Adopt A Family Income", # 4.420.002.000
        "Adopt a Vet", # 3.021.040.000
        "Adopt a Vet Expense", # 5.520.002.100
        "Adopt a Vet Income", # 4.420.002.100
        "Arlington Food Pantry Fund", # 3.021.060.000
        "Arlington Food Pantry Fund Expense", # 5.520.004.000
        "Arlington Food Pantry Fund Income", # 4.420.004.000
        "Housing Corp. of Arlington", # 3.021.180.000
        "Housing Corp. of Arlington Expense", # 5.520.019.010
        "Housing Corp. of Arlington Income", # 4.420.019.010
        "Neighbors In Need", # 3.021.220.000
        "Neighbors In Need Expense", # 5.520.025.000
        "Neighbors In Need Income", # 4.420.025.000
        "One Great Hour of Sharing", # 3.021.240.000
        "One Great Hour of Sharing Expense", # 5.520.027.000
        "One Great Hour of Sharing Income", # 4.420.027.000
        "Outreach Fund", # 3.010.000.000
        "Outreach Fund Designated Expense", # 5.510.000.030
        "Outreach Fund Designated Income", # 4.410.000.030
        "Outreach Fund Expense", # 5.003.000.000
        "Outreach Fund General Fund Income", # 4.410.000.010
        "Outreach Fund Hayes Interest Income", # 4.410.000.020
        "Outreach Fund Income", # 4.410.000.000
        "Relief Fund", # 3.021.300.000
        "Relief Fund Expense", # 5.520.019.020
        "Relief Fund Income", # 4.420.019.020
        "UCC Christmas Fund", # 3.021.380.000
        "UCC Christmas Fund Expense", # 5.520.031.100
        "UCC Christmas Fund Income", # 4.420.031.100
    ],
    "property": [
        "Emergency Property Fund", # 3.032.000.000
        "Emergency Property Fund Expense", # 5.567.000.000
        "Emergency Property Fund Income", # 4.467.000.000
        "Church Grounds", # 5.004.003.004
        "Church Maintenance", # 5.004.003.000
        "Custodial Service", # 5.004.004.003
        "Custodial Supplies", # 5.004.003.006
        "Electric", # 5.004.001.003
        "Emergency Property Fund Contribution", # 5.004.003.100
        "Gas", # 5.004.001.002
        "Oil", # 5.004.001.001
        "Parsonage Electric", # 5.001.004.500
        "Parsonage Grounds", # 5.001.004.600
        "Parsonage Maintenance", # 5.001.004.400
        "Parsonage Oil", # 5.001.004.100
        "Parsonage Water/Sewer", # 5.001.004.300
        "Telephone", # 5.004.001.004
        "Water/Sewer", # 5.004.001.005
    ],
    "education": [
        "Christian Education", # 5.002.001.000
        "Youth Fund", # 3.021.420.000
        "Youth Fund Income", # 4.420.033.000
        "Youth Fund Expense", # 5.520.033.000
    ],
    "stewardship": [
        "Environmental Stewardship", # 3.021.120.000
        "Environmental Stewardship Income", # 4.420.010.000
        "Environmental Stewardship Expense", # 5.520.010.050
    ],
    "worship": [
        "Flower Fund", # 3.021.140.000
        "Flower Fund Expense", # 5.520.013.050
        "Flower Fund Income", # 4.420.013.050
        "Additional Pastor Related Expenses", # 5.001.004.050
        "Pulpit Supply", # 5.001.004.080
        "Worship", # 5.009.003.050
    ],
    "administration": [
        "Additional Property & Search Expenses", # 5.009.010.001
        "Association Dues", # 5.003.003.000
        "Bank Service Charges", # 5.009.004.001
        "Interchurch", # 5.003.002.000
        "Office Expense", # 5.008.001.000
        "Parsonage Basic Telephone", # 5.001.003.005
        "Pastoral Discretionary Expenses", # 5.001.004.070
        "Pastor's Auto Allowance", # 5.001.003.001
        "Pastor's Books/Cont Ed Expense", # 5.001.003.003
        "Pastor's Furnishings", # 5.001.003.002
        "Payroll Services", # 5.009.004.009
        "Property/Liability Insurance", # 5.004.002.001
        "Social Media / Communications", # 5.008.001.010
        "Workers Comp. Insurance", # 5.004.002.002
        "Special Event", # 3.021.360.000
        "Special Event Expense", # 5.520.030.500
        "Special Event Income", # 4.420.030.500
        "Women's Guild", # 3.021.400.000
        "Women's Guild Expense", # 5.520.032.100
        "Women's Guild Income", # 4.420.032.100
    ],
    "membership": [
        "Membership", # 5.009.003.000
    ],
    "music": [
        "Music", # 5.009.003.100
        "Music Fund", # 3.021.200.000
        "Music Fund Income", # 4.420.023.050
        "Music Fund Expense", # 5.520.023.050
        "Organ Restoration", # 3.021.260.000
        "Organ Restoration Income", # 4.420.028.000
        "Organ Restoration Expense", # 5.520.028.000
    ],
    "hospitality": [
        "Hospitality Fund", # 3.021.160.000
        "Hospitality Fund Income", # 4.420.019.000
        "Hospitality Fund Expense", # 5.520.019.000
    ],
    "ignore": [
        "Cambridge Savings Bank Checking", # 1.010.002.000
        "UCF Moderate Balanced Fund (Legacy)", # 1.030.002.001
        "UCF Moderate Balanced Fund (Hayes)", # 1.030.002.002
        "UCF Moderate Balanced Fund (Skinner/Hall)", # 1.030.002.003
        "UCF Moderate Balanced Fund (Memorial)", # 1.030.002.004
        "UCF Moderate Balanced Fund (PSCC)", # 1.030.002.005
        "T Rowe Price Equity Income Fund (Jackson)", # 1.030.005.000
        "Domini Social Equity Fund (Jennings)", # 1.030.005.020
        "Cambridge Savings Bank CD (Smith)", # 1.030.005.030
        "ManuLife (Capital Campaign 2009)", # 1.030.005.040
        "Schwab One Account", # 1.030.006.000
        "Cash", # 1.060.000.000
        "A Place to Grow Security Deposit", # 2.020.007.000
        "Pastor Home Equity Liability", # 2.030.000.000
        "Capital Campaign 2009 Fund", # 3.030.000.000
        "Capital Campaign 2009 Fund Expense", # 5.565.000.000
        "Capital Campaign 2009 Fund Income", # 4.465.000.000
        "Capital Campaign 2009 Fund Supplement Income", # 4.465.500.000
        "Capital Campaign 2009 Return", # 3.070.180.000
        "Capital Campaign 2009 Return Expense", # 5.700.180.000
        "Capital Campaign 2009 Return Income", # 4.700.180.000
        "Capital Fund", # 3.005.000.050
        "Capital Fund Expense", # 5.560.000.000
        "Capital Fund Income", # 4.460.000.000
        "Crockett Memorial", # 3.055.040.000
        "Crockett Memorial Expense", # 5.535.020.010
        "Crockett Memorial Income", # 4.435.020.010
        "Crockett Memorial Return", # 3.070.040.000
        "Crockett Memorial Return Expense", # 5.700.040.000
        "Crockett Memorial Return Income", # 4.700.040.000
        "Deacons Fund", # 3.015.000.000
        "Deacons Fund Expense", # 5.515.000.000
        "Deacons Fund Income", # 4.415.000.000
        "Deacons Fund Skinner/Hall Income", # 4.415.000.010
        "Deacons Fund Smith Income", # 4.415.000.020
        "Departure Gift", # 3.021.080.000
        "Departure Gift Expense", # 5.520.008.100
        "Departure Gift Income", # 4.420.008.100
        "Designated Gift", # 3.021.100.000
        "Designated Gift Expense", # 5.520.008.050
        "Designated Gift Income", # 4.420.008.050
        "A Place to Grow Income", # 4.002.000.000
        "Christmas Envelope", # 4.001.007.001
        "Church School", # 4.001.004.000
        "Country Dance Society Income", # 4.002.004.000
        "Easter Envelope", # 4.001.007.003
        "Education Dir. FICA", # 5.002.002.002
        "Education Dir. Salary", # 5.002.002.001
        "Folk Arts Center Income", # 4.002.007.000
        "General Fund", # 3.005.000.000
        "Gift", # 4.001.002.000
        "Holiday Fair Income", # 4.005.001.000
        "Home Equity/Compensation", # 5.001.003.007
        "Initial Payment & Assoc. Dues", # 4.001.005.000
        "Life and Disability Insurance", # 5.001.002.004
        "Loose Collection", # 4.001.003.000
        "Misc Income", # 4.006.000.000
        "Miscellaneous Rental Income", # 4.002.020.000
        "Office Personnel Compensation", # 5.008.002.001
        "Office Personnel FICA", # 5.008.002.002
        "Organist Compensation", # 5.001.005.001
        "Organist FICA", # 5.001.005.002
        "Other Fundraising Income", # 4.005.005.000
        "Outreach Fund Contribution", # 5.003.004.000
        "Parental Leave Fund Contribution", # 5.001.004.020
        "Pastor's Annuity", # 5.001.002.001
        "Pastor's FICA Reimbursement", # 5.001.001.002
        "Pastor's FSA expense", # 5.001.002.005
        "Pastor's Health Insurance", # 5.001.002.003
        "Pastor's Salary", # 5.001.001.001
        "Philharmonic Society of Arlington Income", # 4.002.010.000
        "Pledges", # 4.001.001.000
        "Prior Year Payment", # 4.001.001.003
        "Royal Scottish Dance Team Income", # 4.002.003.000
        "Rummage Sale Income", # 4.005.004.000
        "Sabbatical Fund Contribution", # 5.001.004.000
        "Thanksgiving Envelope", # 4.001.007.004
        "UCF Moderate Balanced Fund", # 4.004.002.000
        "Vox Lucens/Jay Lane Income", # 4.002.015.000
        "Youth Choir Dir Comp", # 5.002.002.004
        "Youth Choir Dir FICA", # 5.002.002.005
        "Hayes Memorial", # 3.055.060.000
        "Hayes Memorial Expense", # 5.535.030.000
        "Hayes Memorial Income", # 4.435.030.000
        "Hayes Memorial Return", # 3.070.060.000
        "Hayes Memorial Return Expense", # 5.700.060.000
        "Hayes Memorial Return Income", # 4.700.060.000
        "Jackson Legacy", # 3.050.020.000
        "Jackson Legacy Expense", # 5.535.034.000
        "Jackson Legacy Income", # 4.003.005.006
        "Jackson Legacy Return", # 3.070.020.000
        "Jackson Legacy Return Expense", # 5.700.020.000
        "Jackson Legacy Return Income", # 4.700.020.000
        "Jennings Memorial", # 3.055.080.000
        "Jennings Memorial Expense", # 5.535.034.010
        "Jennings Memorial Income", # 4.435.034.010
        "Jennings Memorial Return", # 3.070.080.000
        "Jennings Memorial Return Expense", # 5.700.080.000
        "Jennings Memorial Return Income", # 4.700.080.000
        "Legacy Fund", # 3.005.000.300
        "Legacy Fund Expense", # 5.545.000.000
        "Legacy Fund Income", # 4.445.000.000
        "Legacy Return", # 3.070.160.000
        "Legacy Return Expense", # 5.700.160.000
        "Legacy Return Income", # 4.700.160.000
        "Memorial Fund", # 3.035.000.000
        "Memorial Fund Expense", # 5.535.000.000
        "Memorial Fund Income", # 4.435.000.000
        "Memorial Return", # 3.070.170.000
        "Memorial Return Expense", # 5.700.170.000
        "Memorial Return Income", # 4.700.170.000
        "Parental Leave Fund", # 3.021.270.000
        "Parental Leave Fund Expense", # 5.520.028.010
        "Parental Leave Fund Income", # 4.420.028.010
        "Prepaid Pledges", # 3.021.280.000
        "Prepaid Pledges Expense", # 5.520.028.001
        "Prepaid Pledges Income", # 4.420.028.025
        "PSCC Legacy Fund", # 3.060.000.000
        "PSCC Legacy Fund Expense", # 5.595.000.000
        "PSCC Legacy Fund Income", # 4.495.000.000
        "PSCC Legacy Return", # 3.070.200.000
        "PSCC Legacy Return Expense", # 5.700.200.000
        "PSCC Legacy Return Income", # 4.700.200.000
        "Roof Self-Loan", # 3.005.000.150
        "Roof Self-Loan Expense", # 5.560.000.100
        "Roof Self-Loan Income", # 4.460.000.100
        "Sabbatical Fund", # 3.021.320.000
        "Sabbatical Fund Expense", # 5.520.028.100
        "Sabbatical Fund Income", # 4.420.028.100
        "Sarah's Circle", # 3.021.340.000
        "Sarah's Circle Expense", # 5.520.028.200
        "Sarah's Circle Income", # 4.420.028.200
        "Skinner/Hall Memorial", # 3.055.120.000
        "Skinner/Hall Memorial Expense", # 5.535.063.000
        "Skinner/Hall Memorial Income", # 4.435.063.000
        "Skinner/Hall Memorial Return", # 3.070.120.000
        "Skinner/Hall Memorial Return Expense", # 5.700.120.000
        "Skinner/Hall Memorial Return Income", # 4.700.120.000
        "Smith Memorial", # 3.055.140.000
        "Smith Memorial Expense", # 5.003.001.010
        "Smith Memorial Income", # 4.003.001.010
        "Smith Memorial Return", # 3.070.140.000
        "Smith Memorial Return Expense", # 5.700.140.000
        "Smith Memorial Return Income", # 4.700.140.000
    ]
}
