#!/usr/bin/env python

# pylint: disable=missing-docstring

import re
import json

import number
import amount
import date

################################################################

def clean(string):
    if string is None:
        return None
    string = re.sub(r"\s+", ' ', string)
    return string.strip()

################################################################

def id_validate(id_):
    if re.match('^[0-9]+$', id_) is not None:
        return id_
    else:
        raise ValueError("Invalid id " + id_)

def is_id(id_):
    try:
        return id_validate(id_) != ''
    except ValueError:
        return False

################################################################
################################################################

class Entry(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, line=None):
        self.id_ = None
        self.type_ = None
        self.number_ = None
        self.name_ = None
        self.date_ = None
        self.debit_ = None
        self.credit_ = None
        self.comment_ = None
        self.detail_ = None
        self.posted_ = None
        if line is not None:
            self.load(line)

    def id(self, value=None):
        # pylint: disable=invalid-name
        value = id_validate(clean(value))
        if value is not None:
            self.id_ = value
        return self.id_

    def type(self, value=None):
        value = clean(value)
        if value is not None:
            self.type_ = value
        return self.type_

    def number(self, value=None):
        value = number.fmt(clean(value))
        if value is not None:
            self.number_ = value
        return self.number_

    def name(self, value=None):
        value = clean(value)
        if value is not None:
            self.name_ = value
        return self.name_

    def date(self, value=None):
        value = date.fmt(value)
        if value is not None:
            self.date_ = value
        return self.date_

    def debit(self, value=None):
        value = amount.fmt(value)
        if value is not None:
            self.debit_ = value
        return self.debit_

    def credit(self, value=None):
        value = amount.fmt(value)
        if value is not None:
            self.credit_ = value
        return self.credit_

    def comment(self, value=None):
        value = clean(value)
        if value is not None:
            self.comment_ = value
        return self.comment_

    def detail(self, value=None):
        value = clean(value)
        if value is not None:
            self.detail_ = value
        return self.detail_

    def posted(self, value=None):
        value = date.fmt(value)
        if value is not None:
            self.posted_ = value
        return self.posted_

    ################################################################

    def is_debit(self):
        if self.debit_ is None and self.credit_ is None:
            raise ValueError("No credit or debit in transaction "+self.id_)
        return self.debit_ is not None

    def is_credit(self):
        if self.debit_ is None and self.credit_ is None:
            raise ValueError("No credit or debit in transaction "+self.id_)
        return self.credit_ is not None

    ################################################################

    def date_is(self, date_predicate):
        return date_predicate(self.date())

    def debit_is(self, amount_predicate):
        return amount_predicate(self.debit())

    def credit_is(self, amount_predicate):
        return amount_predicate(self.credit())

    def number_is(self, number_predicate):
        return number_predicate(self.number())

    def name_is(self, name_predicate):
        return name_predicate(self.name())

    ################################################################

    def load(self, line):
        line += ['', '', '', '', '', '', '', '', '', '', '']
        self.id(line[0])
        self.type(line[1])
        self.number(line[2])
        self.name(line[3])
        self.date(line[4])
        self.debit(line[5])
        self.credit(line[6])
        self.comment(line[8])
        self.detail(line[9])
        self.posted(line[11])

    def marshall(self):
        return {
            "id": self.id_,
            "type": self.type_,
            "number": self.number_,
            "name": self.name_,
            "date": self.date_,
            "debit": self.debit_,
            "credit": self.credit_,
            "comment": self.comment_,
            "detail": self.detail_,
            "posted": self.posted_
            }

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2)

################################################################
################################################################

def date_key(entry):
    return date.key(entry.date())
