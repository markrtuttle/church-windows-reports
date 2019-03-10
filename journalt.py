import csv

import entryt

# Import names of entry items (should be values of an enum)
from entryt import TID, TYPE, NUMBER, NAME, DATE, DEBIT, CREDIT
from entryt import COMMENTS, DETAIL, POSTED

# Import list of entry items (should be iterator of an enum)
from entryt import ELEMENTS

# Map entry element to header of journal column containing element
ELEMENT_TO_HEADER_MAP = {
    TID: "Trans. #",
    TYPE: "Type",
    NUMBER: "Account #",
    NAME: "Account Name",
    DATE: "Date Occurred",
    DEBIT: "Debit Amt.",
    CREDIT: "Credit Amt.",
    COMMENTS: "Transaction Comments",
    DETAIL: "Line Item Comments",
    POSTED: "Date Posted",
}

class Journal(object):
    """Church Windows journal"""

    def __init__(self, journals=None):
        """Initialize journal with one or more Church Windows journals"""

        # A list of entries in the journal
        self.entries_ = []
        # A mapping entry element to journal column number with element
        self.element_to_column_map = {}

        for journal in journals:
            self.load(journal)

    def map_element_to_column(self, headers):
        """Map entry element to the journal column containing the element"""

        # Map column header to column number
        header_to_column_map = {}
        column = 0
        for header in headers:
            if header: # skip empty columns
                header_to_column_map[header] = column
            column += 1

        # Map entry element to column number
        for element in ELEMENTS:
            header = ELEMENT_TO_HEADER_MAP[element]
            column = header_to_column_map.get(header)
            self.element_to_column_map[element] = column

    def load(self, journal):
        """Parse journal into table"""

        # reset map from entry element to journal column number
        self.element_to_column_map = {}

        headers_parsed = False
        with open(journal) as journal_transactions:
            for line in csv.reader(journal_transactions):
                line.append("") # Ensure line has at least one item
                if headers_parsed:
                    # Skip initial blank lines
                    if not line[0]:
                        continue
                    # Skip trailing summary line
                    if line[0].startswith(" Trans. Count:"):
                        continue
                    entry = entryt.Entry(line, self.element_to_column_map)
                    self.entries_.append(entry)
                else:
                    if line[0] != ELEMENT_TO_HEADER_MAP[TID]:
                        continue
                    self.map_element_to_column(line)
                    headers_parsed = True

    def entries(self):
        return self.entries_

    def dump(self):
        return [entry.dump() for entry in self.entries_]

    ################################################################

    def accumulate(self, date_start, date_end):
        period_credits = {}
        period_debits = {}
        year_credits = {}
        year_debits = {}

        for entry in self.entries():
            number = entry.number()

            period_credits[number] = period_credits.get(number) or 0
            period_debits[number] = period_debits.get(number) or 0
            year_credits[number] = year_credits.get(number) or 0
            year_debits[number] = year_debits.get(number) or 0

            if entry.date_is(date_start, date_end):
                period_credits[number] += entry.credit() or 0
                period_debits[number] += entry.debit() or 0
            if entry.date_is(None, date_end):
                year_credits[number] += entry.credit() or 0
                year_debits[number] += entry.debit() or 0

        return (period_credits, period_debits, year_credits, year_debits)
