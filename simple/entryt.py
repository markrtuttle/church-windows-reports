import amountt
import datet

# An enum for the entry elements
TID = 0
TYPE = 1
NUMBER = 2
NAME = 3
DATE = 4
DEBIT = 5
CREDIT = 6
COMMENTS = 7
DETAIL = 8
POSTED = 9

# Enum elements
ELEMENTS = [TID, TYPE, NUMBER, NAME, DATE, DEBIT, CREDIT,
            COMMENTS, DETAIL, POSTED]

# The transaction types
BILL = "BILL"
DONA = "DONA"
INCM = "INCM"
JRNL = "JRNL"
PYMT = "PYMT"
TYPES = [BILL, DONA, INCM, JRNL, PYMT]

################################################################

class Entry(object):

    def __init__(self, line, element_to_column):
        self.elements = []
        for element in ELEMENTS:
            value = line[element_to_column[element]]
            self.elements.append(value)
        self.elements[DEBIT] = amountt.from_string(self.elements[DEBIT])
        self.elements[CREDIT] = amountt.from_string(self.elements[CREDIT])
        self.elements[DATE] = datet.from_string(self.elements[DATE])
        self.elements[POSTED] = datet.from_string(self.elements[POSTED])
        if self.elements[NUMBER] == '-A/P Vendor-':
            self.elements[NUMBER] = self.elements[NAME]

    ################################################################

    def id(self):
        return self.elements[TID]

    def type(self, value=None):
        if value is None:
            return self.elements[TYPE] or None
        if value not in TYPES:
            return ValueError
        self.elements[TYPE] = value
        return self.elements

    def date(self, value=None):
        if value is None:
            return self.elements[DATE] or None
        # Assuming date is 10 character date yyyy/mm/dd
        self.elements[DATE] = value
        return self.elements

    def number(self, value=None):
        if value is None:
            return self.elements[NUMBER] or None
        # Assuming number is a valid account number
        self.elements[NUMBER] = value
        return self.elements

    def name(self, value=None):
        return self.elements[NAME]

    def comment(self, value=None):
        return self.elements[COMMENTS]

    def debit(self, value=None):
        if value is None:
            return self.elements[DEBIT] or None
        # Assuming value is an integer value
        self.elements[DEBIT] = value
        return self.elements

    def credit(self, value=None):
        if value is None:
            return self.elements[CREDIT] or None
        # Assuming value is an integer value
        self.elements[CREDIT] = value
        return self.elements

    ################################################################

    def type_is(self, values):
        return self.type() in values

    def number_is(self, numbers):
        return self.number() in numbers

    def date_is(self, low=None, high=None):
        val = self.date()
        low_match = low is None or low <= val
        high_match = high is None or val < high
        return low_match and high_match

    def debit_is(self, low=None, high=None):
        val = self.debit()
        if val is None:
            return False
        low_match = low is None or low <= val
        high_match = high is None or val < high
        return low_match and high_match

    def credit_is(self, low=None, high=None):
        val = self.credit()
        if val is None:
            return False
        low_match = low is None or low <= val
        high_match = high is None or val < high
        return low_match and high_match

    ################################################################

    def dump(self):
        elt = self.elements
        elt[DEBIT] = amountt.to_string(elt[DEBIT])
        elt[CREDIT] = amountt.to_string(elt[CREDIT])
        elt[DATE] = datet.to_string(elt[DATE])
        elt[POSTED] = datet.to_string(elt[POSTED])
        return elt
