import sys
import csv
from pprint import pprint

import entryt
from entryt import TID, TYPE, NUMBER, NAME, DATE, DEBIT, CREDIT, COMMENTS
from entryt import DETAIL, POSTED, ROW_LENGTH

class Journal(object):
    """Church Windows journal"""

    def __init__(self, journals=None):
        """Initialize journal with one or more Church Windows journals"""

        # The list of entries in the journal
        # Each entry is a list of values
        self.entries = []

        # Map entry index journal column header
        self.index_to_header_map = {
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
        # Map journal column header to journal column number
        self.header_to_column_map = {}
        # Map entry index to journal column number
        self.index_to_column_map = {}

        for journal in journals:
            self.load(journal)

    def map_header_to_column(self, headers):
        """Map journal column header to journal column number"""

        column = 0
        for header in headers:
            if header: # skip empty columns
                self.header_to_column_map[header] = column
            column += 1

    def map_index_to_column(self):
        """Map entry index to journal column number"""

        for index in range(ROW_LENGTH):
            header = self.index_to_header_map[index]
            column = self.header_to_column_map[header]
            self.index_to_column_map[index] = column

    def load(self, journal):
        """Parse journal into table"""

        # reset map from entry index to journal column number
        self.header_to_column_map = {}
        self.index_to_column_map = {}

        headers_parsed = False
        with open(journal) as handle:
            for line in csv.reader(handle):
                line.append("")
                if headers_parsed:
                    if not line[0]: # skip blank lines
                        continue
                    if line[0].startswith(" Trans. Count:"): # skip summary
                        continue
                    entry = []
                    for index in self.index_to_column_map:
                        column = self.index_to_column_map[index]
                        value = line[column]
                        entry.append(value)
                    entry[DEBIT] = entryt.str2amt(entry[DEBIT])
                    entry[CREDIT] = entryt.str2amt(entry[CREDIT])
                    self.entries.append(entry)
                else:
                    if line[0] != self.index_to_header_map[TID]:
                        continue
                    self.map_header_to_column(line)
                    self.map_index_to_column()
                    headers_parsed = True

    def entry_list(self):
        return self.entries

if __name__ == "__main__":
    journal = Journal(sys.argv)
    pprint(journal.entries)
