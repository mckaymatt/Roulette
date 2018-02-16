#!/usr/bin/env python
__author__ = 'mattmckay'

import collections
import logging
import sys
import unittest

from roulette import (
    Bet, Bin, BinBuilder, InvalidBet, Martingale, NonRandom, Outcome, Passenger57, RouletteGame,
    SevenReds, Simulator, Table, Wheel,
)


class OutcomeTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_Outcome(self):
        """
        A class which performs a unit test of the Outcome class.
        The unit test should create three instances of Outcome, two of which have the same name.
        It should use a number of individual tests to establish that two Outcome with the same
        name will test true for equality, have the same hash code, and establish that the
        win_amount() method works correctly.
        """

        outcome_one = Outcome("A", 1)
        outcome_two = Outcome("A", 1)
        outcome_three = Outcome("B", 2)
        # tests hash equality
        self.assertTrue(outcome_one == outcome_two)
        self.assertTrue(outcome_one != outcome_three)
        self.assertEqual(outcome_one.win_amount(1), 1 )
        self.assertEqual(outcome_three.win_amount(1), 2)

    def tearDown(self):
        pass


class BinTestCase(unittest.TestCase):

    def setUp(self):
            pass

    def test_Bin(self):
        """
        A class which performs a unit test of the Bin class. The unit test should create several
        instances of Outcome, two instances of Bin and establish that Bins can be constructed
        from the Outcomes.
        """

        outcome_three = Outcome("00-0-1-2-3", 6 )
        outcome_four = Outcome("D", 2)
        outcome_five = Outcome("E", 3)
        outcome_six = Outcome("F", 4)

        bin_one = Bin(outcome_three, outcome_four)
        print 'what is bin one?: ', bin_one
        bin_two = Bin(outcome_five, outcome_six)
        print 'what is bin two?: ', bin_two

    def tearDown(self):
        pass


class WheelTestCase(unittest.TestCase):

    def setUp(self):
            pass

    def test_Wheel(self):
        """
        http://www.itmaybeahack.com/book/oodesign-python-2.1/html/roulette/wheel.html#the-random-bin-selection-responsibility

        Wheel Deliverables
        A class which performs a unit test of building the Wheel class. The unit test should create
        several instances of Outcome, two instances of Bin, and an instance of Wheel. The unit test
        should establish that Bins can be added to the Wheel. A Non-Random Random Number Generator
        class, to be used for testing. A class which tests the Wheel and NonRandom class by
        selecting values from a Wheel object.
        """

        outcome_one = Outcome("Red", 1)
        outcome_two = Outcome("Corner", 2)
        outcome_three = Outcome("Black", 3)
        outcome_four = Outcome("Street", 4)

        nonrandom = NonRandom()
        nonrandom.set_seed(1)

        wheel_one = Wheel(nonrandom)
        wheel_one.add_outcome(1, outcome_one)
        wheel_one.add_outcome(2, outcome_two)
        wheel_one.next()

        self.assertTrue(wheel_one.next(), outcome_one )

        # test get_outcome
        self.wheel_two = Wheel(nonrandom)
        BB = BinBuilder()
        BB.build_bins(self.wheel_two)


class BinBuilderTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_BinBuilder(self):

        nonrandom = NonRandom()
        nonrandom.set_seed(1)

        wheel_one = Wheel(nonrandom)

        BB = BinBuilder()
        BB.build_bins(wheel_one)

        # maybe delete since it isn't asked for
        strait = BB.strait_bets()
        split = BB.split_bets()
        street = BB.street_bet()
        corner = BB.corner_bet()
        five = BB.five_bet()
        line = BB.line_bet()
        dozen = BB.dozen_bet()
        column = BB.column_bet()
        even = BB.even_money_bet()

        all_bin_methods_results = [strait, split, street, corner, five, line, dozen, column, even]
        len_all_outcomes = sum(list(len(i) for i in all_bin_methods_results))


class BetTestCase(unittest.TestCase):

    def test_Bin(self):
        outcome_two = Outcome("Corner", 2)
        outcome_three = Outcome("Black", 3)

        bet1 = Bet(10, Outcome("Red", 1))
        bet2 = Bet(10, outcome_two)
        bet3 = Bet(10, outcome_three)

        self.assertTrue(bet1.win_amount() ==20,) # 10 + 10
        self.assertTrue(bet1.lose_amount() == 10) # lose of wager
        self.assertTrue(bet2.win_amount() == 30) # 10*2 + 10
        self.assertTrue(bet2.lose_amount() == 10) # lose of wager
        self.assertTrue(bet3.win_amount() == 40) # 10*3 + 10
        self.assertTrue(bet3.lose_amount() == 10) # lose of wager

        self.assertEqual(str(bet1), "amount on Red (1:1)")


class TableTestCase(unittest.TestCase):

    def test_Table(self):
        tbl = Table(limit=30)
        bet1 = Bet(10, Outcome("Red", 1))
        bet2 = Bet(20, Outcome("Corner", 2))
        bet3 = Bet(30, Outcome("Black", 3))
        bet4 = Bet(40, Outcome("Street", 4))

        self.assertTrue(tbl.is_valid(bet1))
        self.assertTrue(tbl.is_valid(bet3)) # a bet of 30 should be acceptable even with a limit of 30

        self.assertFalse(tbl.is_valid(bet4)) # 40 should not be valid

        tbl.place_bet(bet1)
        tbl.place_bet(bet2)
        self.assertFalse(tbl.is_valid(bet1))

        """
        Test that exception will raise if a bet causes bets to exceed the table limit
        http://www.lengrand.fr/2011/12/pythonunittest-assertraises-raises-error/
        """
        self.assertRaises(InvalidBet, lambda: tbl.place_bet(bet2)) # this should raise an exception

        # test that Table object is iterable
        self.assertTrue(isinstance(tbl, collections.Iterable))

    def test_TableStr(self):
        tbl = Table(limit=30)
        tbl.place_bet(Bet(10, Outcome("Red", 1)))
        self.assertEquals(str(tbl), "['amount on Red (1:1)']")

class GameTestCase(unittest.TestCase):
    """
    This runs the game a few times for testing
    """
    def test_game(self):
        log = logging.getLogger( "GameTestCase.test_game" )

        # make wheel
        self.nonrandom = NonRandom()
        self.nonrandom.set_seed(2)
        self.wheel = Wheel(self.nonrandom)
        # make BinBuilder and build bins for wheel
        bin_builder = BinBuilder()
        bin_builder.build_bins(self.wheel)
        # make table
        table = Table(limit=100)
        # make player
        _p57 = Passenger57(table=table, stake=100, rounds_to_go=100)
        # make game
        self.game = RouletteGame(self.wheel, table)

        # Test NonRandom
        self.assertEqual(id(self.wheel.next()), id(self.wheel.next()))

        # test game cycle with Passenger57
        for i in range(4):
            self.game.cycle(_p57)

class GameRed(unittest.TestCase):
    """
    Tests that
    """
    def setUp(self ):
        self.nonrandom = NonRandom()
        self.nonrandom.set_seed(1) # red
        wheel = Wheel(self.nonrandom)
        self.table = Table(limit=100)
        bin_builder = BinBuilder()
        bin_builder.build_bins(wheel)
        self.game = RouletteGame(wheel, self.table)

class GameBlack(unittest.TestCase):
    def setUp(self):
        # wheel -- returns bin 2
        self.nonrandom = NonRandom()
        self.nonrandom.set_seed(2) # black
        wheel = Wheel(self.nonrandom)
        self.table = Table(limit=100)
        bin_builder = BinBuilder()
        bin_builder.build_bins(wheel)
        self.game = RouletteGame(wheel, self.table)

class MartingaleTestBlack(GameBlack):
    """
    Black wins every time
    """
    def test_black(self):
        _martin = Martingale(table=self.table, stake=100, rounds_to_go=10)
        for i in range(4):
            self.game.cycle(_martin)

        self.assertEqual(_martin.stake, 104)

        # test set_stake and set_rounds
        _martin.set_stake(200)
        self.assertEqual(_martin.stake, 200)
        _martin.set_rounds(20)
        self.assertEqual(_martin.rounds_to_go, 20)

class MartingaleTestRed(GameRed):
    """
    Red loses every time
    """
    def test_Red(self):

        _martin = Martingale(table=self.table, stake=100, rounds_to_go=10)
        self.game.cycle(_martin) ; self.assertEqual(_martin.stake, 99)
        self.game.cycle(_martin) ; self.assertEqual(_martin.stake, 97)
        self.game.cycle(_martin) ; self.assertEqual(_martin.stake, 93)
        self.game.cycle(_martin) ; self.assertEqual(_martin.stake, 85)
        self.game.cycle(_martin) ; self.assertEqual(_martin.stake, 69)

class SimulatorMartingaleRed(GameRed):
    """
    Martingale should lose every round
    """

    def test_simulator_session(self):

        _martin = Martingale(table=self.table, stake=100, rounds_to_go=100)
        sim = Simulator(self.game, _martin)
        self.assertEqual(sim.session()[0:7], [99,97,93,85,69,37,0])

    def test_simulator_gather(self):
        _martin = Martingale(table=self.table, stake=100, rounds_to_go=50)
        sim = Simulator(self.game, _martin)
        sim.gather()
        self.assertEqual(sim.duration, list( 7 for d in range(50)))

    def test_simulator_standard_deviation(self):
        _martin = Martingale(table=self.table, stake=100, rounds_to_go=100)
        sim = Simulator(self.game, _martin)
        self.assertEqual(sim.standard_deviation([2,4,4,4,5,5,7,9]), 2)

class SimulatorP57Black(GameBlack):
    def test_p57_session(self):
        _p57 = Passenger57(table=self.table, stake=100, rounds_to_go=100)
        sim = Simulator(self.game, _p57)
        sim.gather()
        self.assertEqual(sim.duration, list( 250 for d in range(50)))
        self.assertEqual(sim.maxima, list( 350 for d in range(50)))

class SevenRedsGameRed(GameRed):
    def test_sevenreds(self):
        """
        SevenReds should win every other time it plays
        It should not play until 7 rounds have passed
        """
        seq = [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]
        _SR = SevenReds(table=self.table, stake=100, rounds_to_go=100)

        for i in range(76):

            seed = seq.pop(0)
            self.nonrandom.set_seed(seed)
            self.game.cycle(_SR)
            seq.append(seed)
            if i < 7:
                # there should be non betting until round 8
                self.assertEqual(_SR.stake, 100)
        # 5 wins, 5 loses
        self.assertEqual(_SR.stake, 104)

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "GameTestCase.test_game" ).setLevel( logging.DEBUG )

    unittest.main()
