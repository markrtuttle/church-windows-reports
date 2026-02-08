#!/usr/bin/env python3

import json

from cwr import amountt

################################################################


class Budget:
    def __init__(self, budget=None):
        self.budget = {}
        with open(budget, encoding="utf-8") as handle:
            self.budget = json.load(handle)["budget"]
        for number in self.budget:
            self.budget[number] = amountt.from_string(self.budget[number])

    def balance(self, number):
        return self.budget.get(number)

    ################################################################

    def dictionary(self):
        return self.budget

    def string(self):
        return json.dumps(self.dictionary(), indent=2, sort_keys=True)


################################################################
