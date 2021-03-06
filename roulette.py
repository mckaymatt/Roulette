#!/usr/bin/env python
__author__ = 'mattmckay'

import argparse
import math
import random


class Outcome(object):
    """
    In Roulette, each spin of the wheel has a number of Outcomes with bets that will be paid off.
    It is important that we establish hash equality and name equality. E.g. must be only a single ("Black" 1:1)
    """
    def __init__(self, name, odds):
        self.name = str(name)
        self.odds = int(odds)

    def win_amount(self, amount):
        return self.odds * amount

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __str__(self):
        return "%s (%d:1)" % ( self.name, self.odds )


class Bin(object):
    """
    Bin contains a collection of OUTCOMEs which reflect the winning bets that are paid for a particular bin on a
    roulette wheel.
    """
    def __init__(self, *outcomes):
        self.outcomes = frozenset([outcomes])

    def add(self, outcome):
        self.outcomes |= frozenset([outcome])

    def __str__(self):
        return ', '.join( map(str,self.outcomes) )


class Wheel(object):
    """
    Wheel contains the 38 individual bins on the Roulette wheel, plus a random number generator. It can select a Bin at
    random, simulating a spin of a roulette wheel.
    """
    def __init__(self, rng=None):
        if rng == None:
            self.rng = random.Random()
        else:
            self.rng = rng

        self.bins = tuple( Bin() for i in range(38) )
        self.all_outcomes = frozenset()

    def add_outcome(self, number, outcome):
        """
        adds the given OUTCOME to the BIN with the given number.
        """

        self.bins[number].add(outcome)
        self.all_outcomes = self.all_outcomes | frozenset([outcome])

    def next(self):
        """
        returns a Bin selected at random from the wheel.
        """
        return self.rng.choice(self.bins)

    def get(self, bin):
        """
        returns a given bin from the list
        """
        return self.bins[bin]

    def get_outcome(self, name):
        OC = set([  oc for oc in self.all_outcomes if oc.name.lower() == name.lower()  ])
        assert len(OC) == 1
        return OC


class NonRandom(random.Random):
    """
    non-random number generator for testing
    """
    def __init__(self):
        pass

    def set_seed(self, value):
        """
        saves the value as the next value to return
        """
        self.value = value

    def choice(self, seq):
        return seq[self.value]


class BinBuilder(object):

    def __init__(self):
        pass

    def build_bins(self, wheel):
        """
        creates the OUTCOME instances and uses the add_outcome() method to place each OUTCOME in the appropriate BIN
        of the WHEEL.

        There should be separate methods to generate the straight bets, split bets, street bets, corner bets, line bets,
         dozen bets and column bets, even money bets and the special case of zero and double zero.

        The pool of Outcome objects must be reduced so that each outcome object has unique attributes.
        """
        self.wheel = wheel

        outcome_dict = {}
        outcomes_list = self.strait_bets()+\
                       self.split_bets()+\
                       self.street_bet()+\
                       self.corner_bet()+\
                       self.five_bet()+\
                       self.line_bet()+\
                       self.dozen_bet()+\
                       self.column_bet()+\
                       self.even_money_bet()

        # create a name : outcome dict so that there is only one Outcome obj per unique name
        for bo_tup in outcomes_list:
            outcome_dict[bo_tup[1].name] = bo_tup[1]

        for bo_tup in outcomes_list:
            # add the outcomes to wheel using only Outcome objects with unique attributes
            self.wheel.add_outcome(  bo_tup[0]  , outcome_dict[bo_tup[1].name]  )

    def strait_bets(self):
        """
        38 possible bets
        """
        outcome_list = []
        for i in range(1, 37):
            outcome_list.append((i, Outcome(str(i), 35)))

        outcome_list.append((0, Outcome(str(0), 35)))
        outcome_list.append((37, Outcome(str(00), 35)))
        return outcome_list

    def split_bets(self):
        """
        There are 114 split bet combinations
        """
        outcome_list = []
        one_str = lambda x: str("split "+ str(x)+"-"+str(x+1))
        three_str = lambda x: str("split "+ str(x)+"-"+str(x+3))
        plus_one_list = range(1,35,3) + range(2,36,3)
        plus_three_list = range(1, 34)

        for i in plus_one_list:
            outcome_list.append((i, Outcome(one_str(i), 17)))
            outcome_list.append((i+1, Outcome(one_str(i), 17)))
        for i in plus_three_list:
            outcome_list.append((i, Outcome(three_str(i), 17)))
            outcome_list.append((i+3, Outcome(three_str(i), 17)))
        return outcome_list

    def street_bet(self):
        """
        There are 12 possible bets
        """
        outcome_list = []
        row_list = []
        for i in range(1,35,3):
            row_list.append([i, i+1, i+2])

        for i in enumerate(row_list, start=1):
            outcome_name = str("Street "+ "-".join(map(lambda x: str(x), i[1])))
            for j in i[1]:
                outcome_list.append((j, Outcome(outcome_name, 11)))
        return outcome_list

    def corner_bet(self):
        """
        There are 72 of these possible bets
        """
        outcome_list = []
        corner_name_str = lambda x : str("Corner "+ str(x)+"-"+str(x+1)+"-"+str(x+3)+"-"+str(x+4))
        valid_corner_bet_n = range(1,33, 3) + range(2,33, 3)
        for n in valid_corner_bet_n:
            for j in [0,1,3,4]:
                outcome_list.append((n+j, Outcome(corner_name_str(n), 8)))
        return outcome_list

    def five_bet(self):
        """
        There are 5 possible bets
        """
        outcome_list = []

        outcome_list.append((0, Outcome("Five Bet", 6)))
        outcome_list.append((37, Outcome("Five Bet", 6)))
        for i in [1,2,3]:
            outcome_list.append((i, Outcome("Five Bet", 6)))
        return outcome_list

    def line_bet(self):
        """
         There are 11 such combinations
        """
        outcome_list = []
        line_name_str = lambda x : str("line "+ str(x)+"-"+str(x+1)+"-"+str(x+2)+"-"+str(x+3)+"-"+str(x+4)+"-"+str(x+5))
        valid_line_bet_n = range(1,33, 3)
        for n in valid_line_bet_n:
            for j in [0,1,2,3,4,5]:
                outcome_list.append((n+j, Outcome(line_name_str(n), 5)))
        return outcome_list

    def dozen_bet(self):
        """
        There are 3 possible bets
        """
        outcome_list = []
        for d in [1,13,25]:
            dozen_string = "Dozen " + str(d)+"-"+str(d+11)
            for j in range(0, 12):
                outcome_list.append((d+j, Outcome(dozen_string, 2)))
        return outcome_list

    def column_bet(self):
        """
        There are 3 possible bets
        """
        outcome_list = []
        for i in [1,2,3]:
            column_string = "Column " + str(i)
            for j in range(i, 37, 3):
                outcome_list.append((j, Outcome(column_string, 2)))
        return outcome_list

    def even_money_bet(self):
        outcome_list = []
        even_dict = {}
        even_dict["Red"] =  [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        even_dict["Black"] = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        even_dict["Even"] = range(1, 37, 2)
        even_dict["Odd"] = range(2, 37, 2)
        even_dict["High"] = range(1,19)
        even_dict["Low"] = range(19,37)
        for k in even_dict.keys():
            for i in even_dict[k]:
                outcome_list.append((i, Outcome(k, 1)))
        return outcome_list


class Bet(object):
    """
    Bet associates an amount and an Outcome. We can also associate a Bet with a Player.
    class which produces references to Outcomes as needed.
    """

    def __init__(self, amount, outcome):
        self.amount = amount
        self.outcome = outcome

    def win_amount(self):
        return self.amount + self.outcome.win_amount(self.amount)

    def lose_amount(self):
        return self.amount

    def __str__(self):
        return "amount on " + str(self.outcome)


class Table(object):
    """
    """
    def __init__(self, limit):
        assert type(limit) == int
        self.limit = limit
        self.bets = []

    def is_valid(self, bet):
        bets_total = sum(list(b.amount for b in self.bets))
        if bets_total + bet.amount <= self.limit:
            return True
        else:
            return False

    def place_bet(self, bet):

        self.bets.append(bet)
        bets_total = sum(list(b.amount for b in self.bets))
        if bets_total > self.limit:
            raise InvalidBet(self.bets)

    def remove_bet(self):
        self.bets = self.bets[1::]

    def __iter__(self):
        return self.bets[:].__iter__()

    def __str__(self):
        return str(list( str(b) for b in self.bets ) )


class InvalidBet(Exception):
    """
    Error raised when the bet limit is exceeded. This shouldn't normally happen.
    """
    def __init__(self, bets):
        self.bets = bets

    def __str__(self):
        return  "The total of all bets has exceeded the bet limit. This shouldn't normally happen. Bets = %s Sum = %i" %\
              (str(list(b.amount for b in self.bets)), sum(list(b.amount for b in self.bets)) )


class Player(object):
    """
    Abstract player superclass
    """
    def __init__(self, table, stake=100, rounds_to_go=100):
        self.table = table
        self.stake = stake
        self.rounds_to_go = rounds_to_go

    def playing(self, deduct_round=True):
        """
        Returns True while ROUNDSTOGO is not 0
        """
        return self.rounds_to_go > 0 and self.stake > 0

    def place_bets(self):
        """
        deducts amount from stake and places BET on table
        """
        raise NotImplementedError

    def is_valid(self, bet):
        """
        checks with TABLE to see if the BET is valid
        """
        return self.table.is_valid(bet)

    def reset_class_defaults(self):
        pass

    def winners(self, wheel_obj, winning_bin):
        pass

    def win(self, bet):
        self.stake += bet.win_amount()

    def lose(self, bet):
        pass

    def set_stake(self, stake):
        self.stake = stake

    def set_rounds(self, rounds_to_go):
        self.rounds_to_go = rounds_to_go


class Martingale(Player):
    """
    Martingale is a Player as described: https://en.wikipedia.org/wiki/Martingale_(betting_system)
    """
    _base_wager = 1
    _loss_count = 0
    def __init__(self, table, stake, rounds_to_go):
        Player.__init__(self, table, stake, rounds_to_go)
        self.base_wager = 1
        self.loss_count = 0
        self.bet_multiple = 2**self.loss_count # this should always equal 2**loss_count
        self.black = Outcome("Black", 1)

    def place_bets(self):
        """
        makes a BET based on the martingale strategy and the LOSSCOUNT
        """
        self.bet_multiple = 2**self.loss_count

        _bet =  Bet(self.base_wager*self.bet_multiple, self.black)
        # print "__1__",self.stake, _bet.amount

        if (self.stake - _bet.amount) < 0:
            _bet =  Bet(self.stake, self.black)

        if self.is_valid(_bet):
            self.stake -= _bet.amount
            self.table.place_bet(_bet)


    def win(self, bet):
        self.loss_count = 0
        self.stake += bet.win_amount()

    def lose(self, bet):
        self.loss_count += 1


    def reset_class_defaults(self):
        self.base_wager = Martingale._base_wager
        self.loss_count = Martingale._loss_count


class SevenReds(Martingale):
    """
    SevenReds is a Martingale player who only places bets after the wheel has spun red 7 times
    """
    def __init__(self, table, stake, rounds_to_go):
        Martingale.__init__(self, table, stake, rounds_to_go)
        self.redCount = 7

    def playing(self):
        if self.rounds_to_go > 0 and self.stake > 0 and self.redCount == 0:
            self.redCount = 7
            return True
        else:
            return False

    def winners(self, wheel_obj, winning_bin):
        """
        The winning_bin is the BIN selected by WHEEL.
        I also include the wheel_object just because it makes it easier to compare outcomes when we
        have access to the get_outcome method. Object equality yo! Might want to refactor that...
        """
        _red_outcome = Outcome("Red", 1)
        singleton_red_outcome = wheel_obj.get_outcome(_red_outcome.name)
        if singleton_red_outcome.pop() in winning_bin.outcomes:
            self.redCount -= 1
        else:
            self.redCount = 7


class Passenger57(Player):
    """
    Passenger57 always bets black
    """
    def __init__(self, table, stake, rounds_to_go):
        Player.__init__(self, table, stake, rounds_to_go)
        self.black = Outcome("Black", 1)

    def place_bets(self):
        _bet = Bet(1, self.black)
        if self.is_valid(_bet):
            self.stake -= _bet.amount
            self.table.place_bet(_bet)


class RouletteGame(object):
    """
    Manages the sequence of actions that defines the game of Roulette. Responsible for:
        Notifying PLAYER to place bets
        spinning the wheel
        resolving the BETs are actually present on the table
    """
    def __init__(self, wheel, table):
        self.wheel = wheel
        self.table = table

    def notify_player(self, player, wheel_obj, winning_bin ):
        player.winners(wheel_obj, winning_bin )

    def cycle(self, player):

        if player.playing():
            # command player to place a bet
            player.place_bets()

        # this returns an bin class object which contains Outcomes.OUTCOMES are an attribute of BIN
        win_bin = self.wheel.next()

        for bet in self.table:
            outcomes_matching_bet_name = self.wheel.get_outcome(bet.outcome.name)
            assert len(outcomes_matching_bet_name) == 1
            if outcomes_matching_bet_name.pop() in win_bin.outcomes:
                player.win(bet)
            else:
                player.lose(bet)

            # remove the bet
            self.table.remove_bet()
        else:
            # send winning bin to play so they can see winning the outcomes even when they don't play
            self.notify_player(player, wheel_obj=self.wheel, winning_bin=win_bin)
            player.rounds_to_go -= 1 # reduce roundToGo


class Simulator(object):

    def __init__(self, game, player):
        self.init_duration = 250 # cycles that a player
        self.init_stake = 100
        self.samples = 50
        self.duration = []
        self.maxima = []
        self.player = player
        self.game = game

    def session(self):
        stake_vales = []

        while self.player.rounds_to_go != 0 and self.player.stake != 0:
            self.game.cycle(self.player)
            stake_vales.append(self.player.stake)
        return stake_vales

    def gather(self):
        for i in range(self.samples):
            self.reset_player()
            SV = self.session()
            # print "Stake Values", SV

            self.duration.append(len(SV)) # length of the session List - duration
            self.maxima.append(max(SV)) # the maximum value in the session List -  maximum metrics
        self.report()

    def reset_player(self):
        self.player.set_stake(self.init_stake)
        self.player.set_rounds(self.init_duration)
        self.player.reset_class_defaults()

    def get_average(self, L):
        return float(sum(L)) / len(L)

    def standard_deviation(self, L):
        _avg = self.get_average(L)
        dif_sqrd = map(lambda x : ((x - _avg)**2 ), L)
        return math.sqrt(float(sum(dif_sqrd)) / len(dif_sqrd))

    def report(self):
        print "-%s's- \nMaxima Average: [ %f ] \nMaxima Standard Deviation: [ %f ] "  % \
              (self.player.__class__.__name__, self.get_average(self.maxima), self.standard_deviation(self.maxima))
        print "Duration Average: [ %f ] \nDuration Standard Deviation: [ %f ] " %\
              (self.get_average(self.duration), self.standard_deviation(self.duration))
        print "\nMaxima: ", self.maxima
        print "\n\nDuration: ", self.duration, "\n\n"


class RunGame(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='This program simulates rounds of Roulette')
        parser.add_argument('-s', '--stake', help='Initial player stake', default=100, type=int, required=False)
        parser.add_argument('-r', '--rounds', help='Rounds to conduct', default=100, type=int, required=False)
        parser.add_argument('-l', '--limit', help='Table bet limit', default=100, type=int, required=False)
        args = parser.parse_args()

        wheel = Wheel()
        self.table = Table(limit=args.limit)
        bin_builder = BinBuilder()
        bin_builder.build_bins(wheel)
        self.game = RouletteGame(wheel, self.table)

        print 'Starting Stake: (%d) - Rounds: (%d) - Table Limit: (%d) \n' % \
              (args.stake, args.rounds, args.limit)

        _martin = Martingale(table=self.table, stake=args.stake, rounds_to_go=args.rounds)
        sim = Simulator(self.game, _martin)
        sim.gather()

        _7R = SevenReds(table=self.table, stake=args.stake, rounds_to_go=args.rounds)
        sim = Simulator(self.game, _7R)
        sim.gather()

        # p57 = Passenger57(table=self.table, stake=100, rounds_to_go=100)
        # for i in range(95):
        #     self.game.cycle(p57)

if __name__ == '__main__':
    RunGame()
