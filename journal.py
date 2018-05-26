#!/usr/bin/env python

# pylint: disable=missing-docstring

# TODO: Parse using column header titles

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

    def sort(self, entries=None, key=date.key):
        entries = entries or self.entry_
        entries.sort(key=key)

    ################################################################

    def period_entries(self, date_start, date_end, posted_start):
        def in_period(entry_):
            return ((date.le(date_start, entry_.date()) and
                     date.le(entry_.date(), date_end))
                    or
                    (date.lt(entry_.date(), date_start) and
                     date.ge(entry_.posted(), posted_start)))
        entries = self.entry_is(in_period)
        entries.sort(key=entry.date_key)
        return entries


################################################################
