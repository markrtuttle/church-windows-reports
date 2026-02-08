class Layout:
    def __init__(self, width=None):
        self.line_width = width or 80
        self.amount_width = 8
        self.balance_width = 10
        self.comment_width = 35
        self.name_width = 25
        self.name_width_max = 40

    def width(self):
        return self.line_width

    def amount(self):
        return self.amount_width

    def balance(self):
        return self.balance_width

    def comment(self):
        return self.comment_width

    def name(self):
        return self.name_width

    def name_max(self):
        return self.name_width_max
