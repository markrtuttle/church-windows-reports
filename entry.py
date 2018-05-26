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

def is_header(string):
    string = clean(string)
    return string == "Trans. #"

def column_map(headers):
    col_map = {}
    index = 0
    for header in headers:
        try:
            if header:
                key = HEADER_MAP[header]
            else:
                key = None
        except KeyError:
            raise KeyError("Header {} not in header map".format(header))
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
    # pylint: disable=too-many-instance-attributes

    def __init__(self, line=None, col_map=None):
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
        self.payment_method_ = None
        self.check_number_ = None
        self.reconciled_ = None
        self.vendor_ = None
        self.invoice_number_ = None
        self.paid_ = None
        self.due_date_ = None
        self.user_ = None
        self.deposit_slip_ = None
        self.batch_code_ = None
        self.reversed_ = None
        self.corrected_ = None
        if line is not None and col_map is not None:
            self.load(line, col_map)

    def load(self, columns, col_map):
        index = 0
        for col in columns:
            key = col_map[index]
            self.load_key(key, col)
            index += 1

    def load_key(self, key, val):
        if key is None or val is None:
            return
        if key == "id":
            self.id(val)
        elif key == "type":
            self.type(val)
        elif key == "number":
            self.number(val)
        elif key == "name":
            self.name(val)
        elif key == "date":
            self.date(val)
        elif key == "debit":
            self.debit(val)
        elif key == "credit":
            self.credit(val)
        elif key == "comment":
            self.comment(val)
        elif key == "detail":
            self.detail(val)
        elif key == "posted":
            self.posted(val)
        elif key == "payment_method":
            self.payment_method(val)
        elif key == "check_number":
            self.check_number(val)
        elif key == "reconciled":
            self.reconciled(val)
        elif key == "vendor":
            self.vendor(val)
        elif key == "invoice_number":
            self.invoice_number(val)
        elif key == "paid":
            self.paid(val)
        elif key == "due_date":
            self.due_date(val)
        elif key == "user":
            self.user(val)
        elif key == "deposit_slip":
            self.deposit_slip(val)
        elif key == "batch_code":
            self.batch_code(val)
        elif key == "reversed":
            self.reversed(val)
        elif key == "corrected":
            self.corrected(val)

    ################################################################

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

    def payment_method(self, value=None):
        value = clean(value)
        if value is not None:
            self.payment_method_ = value
        return self.payment_method_

    def check_number(self, value=None):
        value = clean(value)
        if value is not None:
            self.check_number_ = value
        return self.check_number_

    def reconciled(self, value=None):
        value = clean(value)
        if value is not None:
            self.reconciled_ = value
        return self.reconciled_

    def vendor(self, value=None):
        value = clean(value)
        if value is not None:
            self.vendor_ = value
        return self.vendor_

    def invoice_number(self, value=None):
        value = clean(value)
        if value is not None:
            self.invoice_number_ = value
        return self.invoice_number_

    def paid(self, value=None):
        value = clean(value)
        if value is not None:
            self.paid_ = value
        return self.paid_

    def due_date(self, value=None):
        value = clean(value)
        if value is not None:
            self.due_date_ = value
        return self.due_date_

    def user(self, value=None):
        value = clean(value)
        if value is not None:
            self.user_ = value
        return self.user_

    def deposit_slip(self, value=None):
        value = clean(value)
        if value is not None:
            self.deposit_slip_ = value
        return self.deposit_slip_

    def batch_code(self, value=None):
        value = clean(value)
        if value is not None:
            self.batch_code_ = value
        return self.batch_code_

    def reversed(self, value=None):
        value = clean(value)
        if value is not None:
            self.reversed_ = value
        return self.reversed_

    def corrected(self, value=None):
        value = clean(value)
        if value is not None:
            self.corrected_ = value
        return self.corrected_

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

def date_key(entry):
    return date.key(entry.date())
