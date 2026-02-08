import amountt
import datet


def make_detail_format(layout):

    width = layout.width()
    amount_w = layout.amount()
    name_w = layout.name()
    comment_w = layout.comment()
    name_max = layout.name_max()

    format_string = "{{:>{aw}}} {{:>2}}/{{:>2}} {{:<{nw}}} {{:<{cw}}}"
    format_length = lambda: amount_w + 1 + 5 + 1 + name_w + 1 + comment_w

    remaining_width = width - format_length()
    remaining_width = remaining_width if remaining_width > 0 else 0

    name_pad = remaining_width / 10 * 4
    name_pad = name_pad if name_pad < name_max - name_w else name_max - name_w
    name_pad = name_pad if name_pad > 0 else 0

    name_w += name_pad
    comment_w += remaining_width - name_pad

    string = format_string.format(aw=amount_w, nw=name_w, cw=comment_w)
    width = format_length()

    def print_line(amount, date, name, comment):
        amount = amountt.to_string(amount)
        month, day, _ = datet.parse_ymd_string(date)
        name = name[:name_w]
        comment = comment[:comment_w]
        print(string.format(amount, month, day, name, comment))

    def print_rule():
        print("-" * width)

    return (print_line, print_rule)


def entry_line(entry, print_line, credit):
    date = entry.date()
    name = entry.name()
    comment = entry.comment()

    if credit:
        amount = (entry.credit() or 0) - (entry.debit() or 0)
    else:
        amount = (entry.debit() or 0) - (entry.credit() or 0)

    print_line(amount, date, name, comment)


def entry_lines(entries, print_line, credit):
    for entry in entries:
        entry_line(entry, print_line, credit)


def detail(entries, credit=True, layout=None):
    print_line, _ = make_detail_format(layout)
    entry_lines(entries, print_line, credit)
