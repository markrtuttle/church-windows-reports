#!/usr/bin/env python

# pylint: disable=missing-docstring

# TODO: entry state should be a dictionary

import re
import json

import number
import amount
import date

################################################################

HEADER_MAP = {
    "Trans. #": "id",
    "Type": "type",
    "Account #": "number",
    "Account Name": "name",
    "Date Occurred": "date",
    "Debit Amt.": "debit",
    "Credit Amt.": "credit",
    "Transaction Comments": "comment",
    "Line Item Comments": "detail",
    "Date Posted": "posted",
    "Pymt. Method": "payment_method",
    "Check or Ref. #": "check_number",
    "Reconciled": "reconciled",
    "Vendor / Payee": "vendor",
    "Invoice #": "invoice_number",
    "Paid": "paid",
    "Due Date": "due_date",
    "User": "user",
    "Deposit Slip": "deposit_slip",
    "Batch Code": "batch_code",
    "Reversed": "reversed",
    "Corrected": "corrected"
}

KEYS = HEADER_MAP.values()

def is_header(string):
    string = clean(string)
    return string == "Trans. #"

def column_map(headers):
    col_map = {}
    index = 0
    for header in headers:
        if header:
            try:
                key = HEADER_MAP[header]
            except KeyError:
                raise KeyError("Header {} not in header map".format(header))
        else:
            key = None
        col_map[index] = key
        index += 1
    return col_map

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

class Entry(object):
    #  pylint: disable=too-many-public-methods

    def __init__(self, line=None, col_map=None):
        self.element = {}
        if line is not None and col_map is not None:
            self.load(line, col_map)

    def load(self, columns, col_map):
        index = 0
        for col in columns:
            key = col_map[index]
            self.set(key, col)
            index += 1

    def set(self, key, val):
        if key is None:
            return None

        key = clean(key)
        if not key in KEYS:
            raise ValueError("Unknown entry key "+key)

        if val is None:
            return self.element.get(key)

        if key in ["number"]:
            self.element[key] = number.fmt(val)
        elif key in ["credit", "debit"]:
            self.element[key] = amount.fmt(val)
        elif key in ["date", "posted", "date_due"]:
            self.element[key] = date.fmt(val)
        elif key in ["id", "check_number"]:
            self.element[key] = int(clean(val))
        else:
            self.element[key] = clean(val)

        return self.element.get(key)

    ################################################################

    def id(self, val=None):
        #pylint: disable=invalid-name
        return self.set("id", val)
    def type(self, val=None):
        return self.set("type", val)
    def number(self, val=None):
        return self.set("number", val)
    def name(self, val=None):
        return self.set("name", val)
    def date(self, val=None):
        return self.set("date", val)
    def debit(self, val=None):
        return self.set("debit", val)
    def credit(self, val=None):
        return self.set("credit", val)
    def comment(self, val=None):
        return self.set("comment", val)
    def detail(self, val=None):
        return self.set("detail", val)
    def posted(self, val=None):
        return self.set("posted", val)
    def payment_method(self, val=None):
        return self.set("payment_method", val)
    def check_number(self, val=None):
        return self.set("check_number", val)
    def reconciled(self, val=None):
        return self.set("reconciled", val)
    def vendor(self, val=None):
        return self.set("vendor", val)
    def invoice_number(self, val=None):
        return self.set("invoice_number", val)
    def paid(self, val=None):
        return self.set("paid", val)
    def due_date(self, val=None):
        return self.set("due_date", val)
    def user(self, val=None):
        return self.set("user", val)
    def deposit_slip(self, val=None):
        return self.set("deposit_slip", val)
    def batch_code(self, val=None):
        return self.set("batch_code", val)
    def reversed(self, val=None):
        return self.set("reversed", val)
    def corrected(self, val=None):
        return self.set("corrected", val)

    ################################################################

    def is_debit(self):
        if self.debit() is None and self.credit() is None:
            raise ValueError("No credit or debit in transaction "+self.id())
        return self.debit() is not None

    def is_credit(self):
        if self.debit() is None and self.credit() is None:
            raise ValueError("No credit or debit in transaction "+self.id())
        return self.credit() is not None

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

    def marshall(self):
        return self.element

    def dump_jsons(self):
        return json.dumps(self.marshall(), indent=2)

################################################################

def date_key(entry):
    return date.key(entry.date())
