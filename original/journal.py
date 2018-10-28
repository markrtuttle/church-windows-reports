#!/usr/bin/env python

# pylint: disable=missing-docstring

import json
import csv

import date
import entry

################################################################

class Journal(object):

    def __init__(self, journals=None):
        self.entry_ = []
        if journals is not None:
            for journal in journals:
                self.load(journal)

    def load(self, journal):
        with open(journal) as handle:
            for line in csv.reader(handle):
                line += ['']
                if entry.is_header(line[0]):
                    column_map = entry.column_map(line)
                    continue
                if entry.is_id(line[0]):
                    self.entry_.append(entry.Entry(line, column_map))

    ################################################################

    def date_is(self, date_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if ent.date_is(date_predicate)]

    def debit_is(self, amount_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if ent.debit_is(amount_predicate)]

    def credit_is(self, amount_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if ent.credit_is(amount_predicate)]

    def amount_is(self, amount_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if
                ent.debit_is(amount_predicate)
                or
                ent.credit_is(amount_predicate)]

    def number_is(self, number_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if ent.number_is(number_predicate)]

    def name_is(self, name_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if ent.name_is(name_predicate)]

    def entry_is(self, entry_predicate, entries=None):
        entries = entries or self.entry_
        return [ent for ent in entries if entry_predicate(ent)]


    ################################################################

    def dump_jsons(self, entries=None):
        entries = entries or self.entry_
        return json.dumps([entry_.marshall() for entry_ in entries],
                          indent=2)

    def sort(self, entries=None, key=entry.date_key):
        entries = entries or self.entry_
        entries.sort(key=key)

    ################################################################

    def entries(self):
        return self.entry_

################################################################

MONTH = {date.month_name(n): n for n in range(1, 13)}

def parse_date_generated(string):
    try:
        parts = [stng.strip(',') for stng in string.split()]
        (_, month, day, year) = parts
        return (MONTH[month], int(day), int(year))
    except (ValueError, KeyError):
        return None

def is_date_generated(string):
    return parse_date_generated(string) is not None
