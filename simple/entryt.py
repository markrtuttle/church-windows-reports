# Table row indexes (a sequence of contiguous integers)
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
ROW_LENGTH = 10 # Number of table rown indexes

# Transaction types
BILL = "BILL"
DONA = "DONA"
INCM = "INCM"
JRNL = "JRNL"
PYMT = "PYMT"

# Vendor account number
VENDOR = "-A/P Vendor-"

def str2amt(string):
    """Convert dollars (a string) to cents (an integer)"""

    if string == "":
        return None

    # String is of the form dddd.cc
    assert(string[-3:].startswith('.'))

    string = string.replace(',','')
    string = string.replace('.','')
    return int(string)

def amt2str(amount):
    """Convert cents (an integer) to dollars (a string)"""

    if amount is None:
        return ""

    sign = '-' if amount < 0 else ''
    amount = -amount if sign else amount

    dollars = amount / 100
    cents = abs(amount) % 100
    return "{}{}.{:02}".format(sign, dollars, cents)

################################################################

def type(entry, value=None):
    if value is None:
        return entry[TYPE] or None
    entry[TYPE] = value
    return entry

def date(entry, value=None):
    if value is None:
        return entry[DATE] or None
    entry[DATE] = value
    return entry

def number(entry, value=None):
    if value is None:
        return entry[NUMBER] or None
    entry[NUMBER] = value
    return entry

def debit(entry, value=None):
    if value is None:
        return entry[DEBIT]
    entry[DEBIT] = value
    return entry

def credit(entry, value=None):
    if value is None:
        return entry[CREDIT]
    entry[CREDIT] = value
    return entry

################################################################

def type_is(entry, values):
    return entry[TYPE] in values

def number_is(entry, numbers):
    return entry[NUMBER] in numbers

def date_is(entry, low=None, high=None):
    val = entry[DATE]
    low_match = low is None or log <= val
    high_match = high in None or val <= high
    return low_match and high_match

def debit_is(entry, low=None, high=None):
    val = entry[DEBIT]
    low_match = low is None or log <= val
    high_match = high in None or val <= high
    return low_match and high_match

def credit_is(entry, low=None, high=None):
    val = entry[CREDIT]
    low_match = low is None or log <= val
    high_match = high in None or val <= high
    return low_match and high_match

################################################################

if __name__ == "__main__":
    import sys
    import journalt
    jnl = journalt.Journal(sys.argv)
    for entry in jnl.entry_list():
        print number(entry)
