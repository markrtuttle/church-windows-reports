#!/usr/bin/env python3

# Parse and organize Vanco data to facilitate bank reconcilation.

import csv
import unittest

#################


def load_csv(filename):
    with open(filename, encoding="utf-8") as data:
        vanco = csv.reader(data)
        rows = list(vanco)
        return (rows[0], rows[1:])


def dump_csv(headers, rows, filename):
    with open(filename, "w", encoding="utf-8") as data:
        writer = csv.writer(data)
        writer.writerow(list(headers))
        for row in rows:
            writer.writerow(row)


##############


def header_index(headers):
    return {hdr: idx for idx, hdr in enumerate(headers)}


def sort_rows_by_column(rows, idx):
    return sorted(rows, key=lambda row: row[idx])


def group_rows_by_column(rows, idx):
    keys = sorted(set(row[idx] for row in rows if row[idx]))
    return [[row for row in rows if row[idx] == key] for key in keys]


def select_columns(rows, idxs):
    def columns(row):
        return [row[idx] for idx in idxs]

    return [columns(row) for row in rows]


def select_columns_by_headers(rows, hdrs, hdridx):
    return select_columns(rows, [hdridx[hdr] for hdr in hdrs])


################


def fees_of_rows(rows, fee_cols):
    def fees(row):
        return sum(float(row[fee_col]) for fee_col in fee_cols)

    return sum(fees(row) for row in rows)


def gross_of_rows(rows, gross_col):
    return sum(float(row[gross_col]) for row in rows)


def net_of_rows(rows, gross_col, fee_cols):
    return gross_of_rows(rows, gross_col) - fees_of_rows(rows, fee_cols)


#################


def append_total_to_rows(rows, total_calculator):
    if not rows:
        return []

    length = len(rows[0])
    assert all(len(row) == length for row in rows)

    rows = [row + [""] for row in rows]
    total = total_calculator(rows)
    rows[-1][-1] = f"{total:.2f}"
    return rows


def append_total_to_headers(hdridx, total_header):
    index = len(hdridx)
    assert total_header not in hdridx.keys()
    assert index not in hdridx.values()
    hdridx[total_header] = index
    return hdridx


def set_total_in_rows(rows, total_calculator, total_column):
    total = total_calculator(rows)
    rows[-1][total_column] = total
    return rows


#################


def append_column(headers, rows, column_header):
    assert headers and rows
    print(len(headers))
    print([len(row) for row in rows])
    assert all(len(row) == len(headers) for row in rows)
    assert column_header not in headers

    headers = headers + [column_header]
    rows = [row + [""] for row in rows]
    return headers, rows


#################

# BANK_HDRS = [
#     'Deposit Date',
#     'ACH/CC',
#     'Member Name',
#     'Fund Name',
#     'Amount',
#     'Discount Amount',
#     'Transaction Fee',
# ]

CW_HDRS = [
    "Date",
    "Process Date",
    "Settlement Date",
    "ACH/CC",
    "Member Name",
    "Fund Name",
    "Amount",
    "Discount Amount",
    "Transaction Fee",
    "Gross",
]


# def bank(vanco_input, bank_output):
#     headers, rows = load_csv(vanco_input)
#     hdridx = header_index(headers)

#     groups = [subgroup
#                  for group in group_rows_by_column(rows, hdridx["Deposit Date"])
#                  for subgroup in group_rows_by_column(group,hdridx["ACH/CC"])]

#     gross_col = hdridx['Amount']
#     fee_cols =  [hdridx[hdr] for hdr in ['Discount Amount', 'Transaction Fee']]
#     def total_calculator(rows):
#         return net_of_rows(rows, gross_col, fee_cols)
#     groups = [ append_total_to_rows(group, total_calculator) for group in groups]
#     hdridx = append_total_to_headers(hdridx, "Deposit")

#     rows = [ row for group in groups for row in group]

#     bank_headers = BANK_HDRS + ["Deposit"]
#     bank_rows = select_columns_by_headers(rows, bank_headers, hdridx)
#     dump_csv(bank_headers, bank_rows, bank_output)


def accumulator(add_cols, sub_cols):
    return lambda row: sum(row[col] for col in add_cols) - sum(row[col] for col in sub_cols)


def set_group_total(group, accumulate, dst_row, dst_col):
    group[dst_row][dst_col] = sum(accumulate(row) for row in group)
    return group


def church_windows(vanco_input, church_windows_output):
    headers, rows = load_csv(vanco_input)
    headers, rows = append_column(headers, rows, "Date")
    headers, rows = append_column(headers, rows, "Gross")
    hdridx = header_index(headers)

    ach, cc = group_rows_by_column(rows, hdridx["ACH/CC"])

    def copy_column(row, src, dst):
        row[dst] = row[src]
        return row

    def set_ach_date(row):
        return copy_column(row, hdridx["Deposit Date"], hdridx["Date"])

    def set_cc_date(row):
        return copy_column(row, hdridx["Settlement Date"], hdridx["Date"])

    ach = [set_ach_date(row) for row in ach]
    cc = [set_cc_date(row) for row in cc]
    rows = ach + cc

    groups = group_rows_by_column(rows, hdridx["Date"])

    gross_col = hdridx["Amount"]
    fee_cols = []

    def total_calculator(rows):
        return net_of_rows(rows, gross_col, fee_cols)

    groups = [set_total_in_rows(group, total_calculator, hdridx["Gross"]) for group in groups]

    rows = [row for group in groups for row in group]

    cw_headers = CW_HDRS
    cw_rows = select_columns_by_headers(rows, cw_headers, hdridx)
    dump_csv(cw_headers, cw_rows, church_windows_output)


def main():
    # bank("vanco2.csv", "bank.csv")
    church_windows("vanco2.csv", "church_windows.csv")


if __name__ == "__main__":
    main()


class Tests(unittest.TestCase):
    def test1(self):
        headers = ["Member Name", "Amount", "Process Date", "Settlement Date", "ACH/CC"]
        rows = [["Name", "25", "3/22/24", "3/26/24", "ACH"]]

        headers1, rows1 = append_column(headers, rows, "Added")
        self.assertEqual(headers1, headers + ["Added"])
        self.assertEqual(rows1, [rows[0] + [""]])

    def test_sort_rows_by_column(self):
        headers0, rows0 = load_csv("test-data.csv")
        rows = sort_rows_by_column(rows0, 7)
        headers1, rows1 = load_csv("test_sort_rows_by_column.csv")
        self.assertEqual(headers1, headers0)
        self.assertEqual(rows1, rows)
