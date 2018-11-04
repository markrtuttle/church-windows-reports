#!/usr/bin/env python

import report_style

def subfund_report(period_name, chart, balance, width):

    # pylint: disable=too-many-arguments

    fund_name = "Special Funds"
    report_style.fund_report(
        fund_name,
        period_name,
        chart.account(chart.number(fund_name)).children(),
        chart,
        balance,
        width=width)

    print

    fund_name = "Investment Return"
    report_style.fund_report(
        fund_name,
        period_name,
        chart.account(chart.number(fund_name)).children(),
        chart,
        balance,
        width=width)
