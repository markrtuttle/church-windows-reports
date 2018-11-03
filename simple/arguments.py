#!/usr/bin/env python

# pylint: disable=misplaced-comparison-constant

import argparse

import datet

################################################################

def command_line_parser():
    """Create the command line parser."""
    parser = argparse.ArgumentParser(
        description='Generate reports from Church Windows data'
    )
    parser.add_argument(
        '--chart',
        default='chart.json',
        metavar='FILE',
        help='Chart of accounts dumped created by make-chart.'
    )
    parser.add_argument(
        '--initial',
        default='initial.json',
        metavar='FILE',
        help='List of initial balances created by make-initial.'
    )
    parser.add_argument(
        '--budget',
        default='budget.json',
        metavar='FILE',
        help='List of budget amounts created by make-budget.'
    )
    parser.add_argument(
        '--journal',
        default=['journal.csv'],
        metavar='FILE',
        nargs='+',
        help=('Journal dumped by Church Windows as a .csv file. '
              '(default: journal.csv)')
    )
    parser.add_argument(
        '--month',
        type=int,
        metavar='MONTH',
        help='Month of the report (default: this month)'
    )
    parser.add_argument(
        '--year',
        type=int,
        metavar='YEAR',
        help='Year of the report (default: this year)'
    )
    parser.add_argument(
        '--date-start',
        metavar='DATE',
        help='Starting date of the report (default: first day of MONTH/YEAR)'
    )
    parser.add_argument(
        '--date-end',
        metavar='DATE',
        help='Ending date of the report (default: last day of MONTH/YEAR)'
    )
    parser.add_argument(
        '--posted-start',
        metavar='DATE',
        help=('Starting "date posted" for entries outside this month '
              '(default: start of MONTH/YEAR)')
    )
    parser.add_argument(
        '--posted-end',
        metavar='DATE',
        help=('Ending "date posted" for entries outside this month '
              '(default: start of MONTH/YEAR)')
    )
    parser.add_argument(
        '--line-width',
        type=int,
        default=80,
        metavar='INT',
        help="Line width for reports. (default: 80)"
    )
    parser.add_argument(
        '--portrait',
        dest='line_width',
        action='store_const',
        const=80,
        help="Format reports for portrait mode."
    )
    parser.add_argument(
        '--landscape',
        dest='line_width',
        action='store_const',
        const=110,
        help="Format reports for landscape mode."
    )
    parser.add_argument(
        '--ministries',
        action='store_true',
        help="Generate reports for ministry accounts."
    )
    parser.add_argument(
        '--no-ministries',
        dest='ministries',
        action='store_false',
        help="Don't generate reports for ministry accounts."
    )
    parser.add_argument(
        '--unassigned-report',
        action='store_true',
        help="Generate reports for unassigned accounts."
    )
    parser.add_argument(
        '--no-unassigned-report',
        dest='unassigned_report',
        action='store_false',
        help="Don't generate reports for unassigned accounts."
    )
    parser.add_argument(
        '--vendor-report',
        action='store_true',
        help="Generate reports for vendor accounts."
    )
    parser.add_argument(
        '--no-vendor-report',
        dest='vendor_report',
        action='store_false',
        help="Don't generate reports for vendor accounts."
    )
    parser.add_argument(
        '--subfunds',
        action='store_true',
        help="Generate reports for subfund accounts."
    )
    parser.add_argument(
        '--no-subfunds',
        dest='subfunds',
        action='store_false',
        help="Don't generate reports for subfund accounts."
    )
    parser.add_argument(
        '--bills',
        action='store_true',
        help="Generate report of material bills."
    )
    parser.add_argument(
        '--no-bills',
        dest='bills',
        action='store_false',
        help="Don't generate report of material bills."
    )
    parser.add_argument(
        '--all-reports',
        action='store_true',
        help="Generate all available reports."
    )
    parser.add_argument(
        '--zeros',
        action='store_true',
        help="Generate reports with zero valued accounts."
    )
    parser.add_argument(
        '--no-zeros',
        dest='zeros',
        action='store_false',
        help="Don't generate reports without zero valued accounts."
    )
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Use a compact format for printing reports'
    )
    parser.add_argument(
        '--newpage',
        action='store_true',
        default=True,
        help='Insert a new page between report sections'
    )
    parser.add_argument(
        '--no-newpage',
        dest='newpage',
        action='store_false',
        help="Don't insert a new page between report sections"
    )
    parser.add_argument(
        '--dump-chart',
        action='store_true',
        help='Dump chart of accounts and exit'
    )
    parser.add_argument(
        '--dump-assigned-accounts',
        action='store_true',
        help='Dump chart of ministry account assignments and exit'
    )
    parser.add_argument(
        '--dump-unassigned-accounts',
        action='store_true',
        help='Dump chart of accounts unassigned to a ministry and exit'
    )
    parser.add_argument(
        '--dump-arguments',
        '--dump-args',
        action='store_true',
        help='Dump current settings of command line arguments and exit'
    )
    return parser

################################################################

def parse():
    # pylint: disable=too-many-branches

    parser = command_line_parser()
    args = parser.parse_args()

    args.date_start = datet.from_string(args.date_start)
    args.date_end = datet.from_string(args.date_end)
    args.posted_start = datet.from_string(args.posted_start)
    args.posted_end = datet.from_string(args.posted_end)

    if args.month is None and args.date_start is not None:
        (args.month, _, _) = datet.parse_ymd_string(args.date_start)
    if args.month is None and args.date_end is not None:
        (args.month, _, _) = datet.parse_ymd_string(args.date_end)
    if args.month is None:
        args.month = datet.this_month()

    if args.year is None and args.date_start is not None:
        (_, _, args.year) = datet.parse_ymd_string(args.date_start)
    if args.year is None and args.date_end is not None:
        (_, _, args.year) = datet.parse_ymd_string(args.date_end)
    if args.year is None:
        args.year = datet.this_year()

    if not (0 <= args.month and args.month <= 12):
        raise ValueError("Invalid month: "+args.month)
    if not (0 <= args.year and args.year <= 3000):
        raise ValueError("Invalid year: "+args.year)

    args.month_name = datet.month_name(args.month)

    if args.date_start is None:
        args.date_start = datet.make_ymd_string(args.month, 1, args.year)
    if args.date_end is None:
        args.date_end = datet.make_ymd_string(args.month, 31, args.year)
    if args.posted_start is None:
        args.posted_start = args.date_start
    if args.posted_end is None:
        args.posted_end = datet.from_string(datet.today_string())

    if args.all_reports:
        args.bills = True
        args.ministries = True
        args.unassigned_report = True
        args.vendor_report = True
        args.subfunds = True

    return args

################################################################
