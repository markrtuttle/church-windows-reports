#!/usr/bin/env python3

import argparse
import csv
import json


def command_line_parser():
    """Create the command line parser."""

    parser = argparse.ArgumentParser(
        description=("Extract initial account balances from prior year's " "final balance statement")
    )
    parser.add_argument(
        "--chart",
        default="chart.csv",
        metavar="CHART",
        help=("Chart of accounts dumped from Church Windows as a CSV file" " (default: %(default)s)"),
    )

    return parser


def scan_chart(file):
    """Scan chart of accounts for initial balances"""

    initial = {}
    with open(file, encoding="utf-8") as csvfile:
        for line in csv.reader(csvfile):
            typ = line[0]
            name = line[2]
            number = line[3]
            balance = line[5]

            if typ in ["Asset", "Liability", "Fund", "Income", "Expense"] and balance != "0.00":
                if typ == "Liability" and number == "":
                    number = name
                initial[number] = balance

    return initial


def main():
    parser = command_line_parser()
    args = parser.parse_args()
    initial = scan_chart(args.chart)
    print(json.dumps({"initial balance": initial}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
