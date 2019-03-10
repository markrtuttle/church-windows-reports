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
            column = element_to_column[element]
            value = None if column is None else line[column]
            self.elements.append(value)
        self.elements[DEBIT] = amountt.from_string(self.elements[DEBIT])
        self.elements[CREDIT] = amountt.from_string(self.elements[CREDIT])
        self.elements[DATE] = datet.from_string(self.elements[DATE])
        self.elements[POSTED] = datet.from_string(self.elements[POSTED])
        if self.elements[NUMBER] == '-A/P Vendor-':
            self.elements[NUMBER] = self.elements[NAME]

    ################################################################

    def id(self):
        # pylint: disable=invalid-name
        return self.elements[TID]

    def type(self):
        return self.elements[TYPE]

    def date(self):
        return self.elements[DATE]

    def posted(self):
        return self.elements[POSTED]

    def number(self):
        return self.elements[NUMBER]

    def name(self):
        return self.elements[NAME]

    def comment(self):
        return self.elements[COMMENTS]

    def debit(self):
        return self.elements[DEBIT]

    def credit(self):
        return self.elements[CREDIT]

    ################################################################

    def type_is(self, values):
        return self.type() in values

    def number_is(self, numbers):
        return self.number() in numbers

    def date_is(self, low=None, high=None):
        val = self.date()
        if val is None:
            return False
        low_match = low is None or low <= val
        high_match = high is None or val <= high
        return low_match and high_match

    def posted_is(self, low=None, high=None):
        val = self.posted()
        if val is None:
            return False
        low_match = low is None or low <= val
        high_match = high is None or val <= high
        return low_match and high_match

    def debit_is(self, low=None, high=None):
        val = self.debit()
        if val is None:
            return False
        low_match = low is None or low <= val
        high_match = high is None or val <= high
        return low_match and high_match

    def credit_is(self, low=None, high=None):
        val = self.credit()
        if val is None:
            return False
        low_match = low is None or low <= val
        high_match = high is None or val <= high
        return low_match and high_match

    def amount_is(self, low=None, high=None):
        return self.debit_is(low, high) or self.credit_is(low, high)

    ################################################################

    def dump(self):
        elt = self.elements
        elt[DEBIT] = amountt.to_string(elt[DEBIT])
        elt[CREDIT] = amountt.to_string(elt[CREDIT])
        elt[DATE] = datet.to_string(elt[DATE])
        elt[POSTED] = datet.to_string(elt[POSTED])
        return elt

    def string(self):
        return "{}".format(self.elements)
