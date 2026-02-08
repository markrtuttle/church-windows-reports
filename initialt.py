#!/usr/bin/env python3

import json

import amountt

################################################################


class Initial(object):

    def __init__(self, initial=None):
        self.initial = {}
        with open(initial) as handle:
            self.initial = json.load(handle)["initial balance"]
        for number in self.initial:
            self.initial[number] = amountt.from_string(self.initial[number])

    def balance(self, number):
        return self.initial.get(number, 0)

    def numbers(self):
        return list(self.initial.keys())

    ################################################################

    def dictionary(self):
        return self.initial

    def string(self):
        return json.dumps(self.dictionary(), indent=2, sort_keys=True)


################################################################
