#!/usr/bin/env python

# pylint: disable=misplaced-comparison-constant

import re
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
        help=('Chart of accounts created by make-chart'
              " (default: %(default)s)")
    )
    parser.add_argument(
        '--initial',
        default='initial.json',
        metavar='FILE',
        help=('List of initial balances created by make-initial'
              " (default: %(default)s)")
    )
    parser.add_argument(
        '--budget',
        default='budget.json',
        metavar='FILE',
        help=('List of budget amounts created by make-budget'
              " (default: %(default)s)")
    )
    parser.add_argument(
        '--journal',
        default=['journal.csv'],
        metavar='FILE',
        nargs='+',
        help=('Journal dumped by Church Windows as a .csv file. '
              " (default: %(default)s)")
    )

    parser.add_argument(
        '--dates',
        nargs='+',
        metavar='DATE',
        help=('Specify start and end dates of the current period with'
              ' one or two dates of the form m or m/y or or m/d/y.'
              ' The default period is the current month.'
              ' If only one date is given, use it for both the start and'
              ' end dates.'
              ' If the month or year is missing, use the current month or year.'
              ' If the day is missing, use the first or last day of the month'
              ' for the start or end of the period.')
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
        '--accounts',
        action='append',
        nargs='*',
        help="Display a list of accounts"
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
        '--vendors',
        action='store_true',
        help="Generate reports for vendor accounts."
    )
    parser.add_argument(
        '--no-vendors',
        dest='vendors',
        action='store_false',
        help="Don't generate reports for vendor accounts."
    )
    parser.add_argument(
        '--all-vendors',
        action='store_true',
        help="Generate reports for all vendor accounts (even with zero balance)."
    )
    parser.add_argument(
        '--unassigned',
        action='store_true',
        help="Generate reports for unassigned accounts."
    )
    parser.add_argument(
        '--no-unassigned',
        dest='unassigned',
        action='store_false',
        help="Don't generate reports for unassigned accounts."
    )

    parser.add_argument(
        '--width',
        type=int,
        default=80,
        metavar='INT',
        help="Line width for reports (default: %(default)s)"
    )
    parser.add_argument(
        '--portrait',
        dest='width',
        action='store_const',
        const=80,
        help="Format reports for portrait mode."
    )
    parser.add_argument(
        '--landscape',
        dest='width',
        action='store_const',
        const=130,
        help="Format reports for landscape mode."
    )

    parser.add_argument(
        '--dump-arguments',
        '--dump-args',
        action='store_true',
        help='Dump current settings of command line arguments and exit'
    )
    return parser

################################################################

def parse_dates(date_list):
    try:
        size = len(date_list)
        if size < 1 or size > 2:
            raise ValueError

        if size == 1:
            date_start = datet.from_string(date_list[0], True)
            date_end = datet.from_string(date_list[0], False)
        else:
            date_start = datet.from_string(date_list[0], True)
            date_end = datet.from_string(date_list[1], False)

        return (date_start, date_end)
    except ValueError:
        raise ValueError("Not a valid list of dates: {}.".format(
            ', '.join(date_list)))

################################################################

def parse():
    # pylint: disable=too-many-branches

    parser = command_line_parser()
    args = parser.parse_args()

    (args.date_start, args.date_end) = parse_dates(args.dates)
    args.posted_start = datet.from_string(args.posted_start)
    args.posted_end = datet.from_string(args.posted_end)

    (mon1, _, _) = datet.parse_ymd_string(args.date_start)
    (mon2, _, _) = datet.parse_ymd_string(args.date_end)
    str1 = datet.month_name(mon1)
    str2 = datet.month_name(mon2)
    if mon1 == mon2:
        args.period_name = str1
    else:
        args.period_name = "{}-{}".format(str1[:3], str2[:3])
    args.month_name = args.period_name

    if args.posted_start is None:
        args.posted_start = args.date_start
    if args.posted_end is None:
        args.posted_end = datet.from_string(datet.today_string())

    def flatten(listoflists):
        """Flatten a list of lists into a list"""
        if listoflists is not None:
            return [item for sublist in listoflists for item in sublist]
        return None
    def clean(string):
        """Replace whitespace with a space and strip whitespace from ends."""
        return re.sub(r'\s+', ' ', string).strip()
    if args.accounts:
        args.accounts = flatten(args.accounts)
        args.accounts = [clean(item) for item in args.accounts]

    return args

################################################################
