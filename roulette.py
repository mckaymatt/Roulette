__author__ = 'mattmckay'

import random


class Outcome():
    """
    In Roulette, each spin of the wheel has a number of Outcomes with bets that will be paid off.

    """
    def __init__(self, name, odds):
        self.name = str(name)
        self.odds = int(odds)

    def winAmount(self, amount):
        return self.odds * amount

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __str__(self):
        return "%s (%d:1)" % ( self.name, self.odds )


class Bin():
    """
    Bin contains a collection of OUTCOMEs which reflect the winning bets that are paid for a particular bin on a
    roulette wheel.
    """
    def __init__(self, * outcomes):
        self.outcomes = frozenset(outcomes)

    def add(self, outcome):
        self.outcomes = self.outcomes | frozenset(outcome)

    def __str__(self):
        return ', '.join( map(str,self.outcomes) )

class Wheel():
    """
    Wheel contains the 38 individual bins on the Roulette wheel, plus a random number generator. It can select a Bin at
    random, simulating a spin of a roulette wheel.
    """
    def __init__(self, rng):
        self.rng = rng
        self.bins = tuple( Bin() for i in range(38) )

    def addOutcome(self, number, outcome):
        """
        adds the given OUTCOME to the BIN with the given number.
        """
        self.bins[number].add(outcome)

    def next(self):
        """
        returns a Bin selected at random from the wheel.
        """
        return random.choice(self.bins)

    def get(self, bin):
        """
        returns a given bin from the list
        """
        return self.bins(bin)

class NonRandom(random.Random):
    """
    non-random number generator for testing
    """
    def __init__(self):
        pass

    def setSeed(self, value):
        """
        saves the value as the next value to return
        """
        self.value = value

    def choice(self, seq):
        return seq[self.value]

class BinBuilder():
    def __init__(self):
        pass

    def buildBins(self, wheel):
        """
        creates the OUTCOME instances and uses the addOutcome() method to place each OUTCOME in the appropriate BIN
        of the WHEEL.
        There should be separate methods to generate the straight bets, split bets, street bets, corner bets, line bets,
         dozen bets and column bets, even money bets and the special case of zero and double zero.
        """
        self.wheel = wheel

    def strait_bets(self):
        for i in range(1, 37):
            self.wheel.addOutcome(i, [str(i), 35])
        self.wheel.addOutcome(0, [str(0), 35])
        self.wheel.addOutcome(37, [str(00), 35])

    def split_bets(self):

        one_str = lambda x: str("split", str(x)+"-"+str(x+1))
        three_str = lambda x: str("split", str(x)+"-"+str(x+3))
        num_list = range(1, 37)
        plus_one_list = range(1,35,3) + range(2,36,3)
        plus_three_list = range(1, 34)

        for i in plus_one_list:
            self.wheel.addOutcome(i, [one_str(i), 17])
            self.wheel.addOutcome(i+1, [one_str(i), 17])
        for i in plus_three_list:
            self.wheel.addOutcome(i, [three_str(i), 17])
            self.wheel.addOutcome(i+3, [three_str(i), 17])

    def street_bet(self):
        row_list = []
        row_maker = lambda x : [x,x+1,x+2]
        for i in range(1,35,3):
            row_list.append(row_maker(i))

        for i in enumerate(row_list, start=1):
            outcome_name = str("Street "+ "-".join(map(lambda x: str(x), i[1])))
            for j in i[1]:
                self.wheel.addOutcome(j, [outcome_name, 11])







