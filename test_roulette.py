#!/usr/bin/env python
__author__ = 'mattmckay'

import sys
from roulette import *
import unittest
import collections
import logging

class OutcomeTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_Outcome(self):

        #A class which performs a unit test of the Outcome class. The unit test should create a three instances of
        #  Outcome, two of which have the same name. It should use a number of individual tests to establish that two
        #  Outcome with the same name will test true for equality, have the same hash code, and establish that the
        #  winAmount() method works correctly.

        outcome_one = Outcome("A", 1)
        outcome_two = Outcome("A", 1)
        outcome_three = Outcome("B", 2)
        #tests hash equality
        self.assertTrue(outcome_one == outcome_two)
        self.assertTrue(outcome_one != outcome_three)
        self.assertEqual(outcome_one.winAmount(1), 1 )
        self.assertEqual(outcome_three.winAmount(1), 2)

    def tearDown(self):
        pass

class BinTestCase(unittest.TestCase):

    def setUp(self):
            pass

    def test_Bin(self):
        # A class which performs a unit test of the Bin class. The unit test should create several instances of Outcome,
        #  two instances of Bin and establish that Bin s can be constructed from the Outcomes.

        outcome_three = Outcome("00-0-1-2-3", 6 )
        outcome_four = Outcome("D", 2)
        outcome_five = Outcome("E", 3)
        outcome_six = Outcome("F", 4)

        bin_one = Bin(outcome_three, outcome_four)
        bin_two = Bin(outcome_five, outcome_six)

    def tearDown(self):
        pass

class WheelTestCase(unittest.TestCase):

    def setUp(self):
            pass

    def test_Wheel(self):

        #http://www.itmaybeahack.com/book/oodesign-python-2.1/html/roulette/wheel.html#the-random-bin-selection-responsibility

        #Wheel Deliverables
        #A class which performs a unit test of building the Wheel class. The unit test should create several instances
        # of Outcome, two instances of Bin, and an instance of Wheel. The unit test should establish that Bins can be
        # added to the Wheel.
        #A Non-Random Random Number Generator class, to be used for testing.
        #A class which tests the Wheel and NonRandom class by selecting values from a Wheel object.

        outcome_one = Outcome("Red", 1)
        outcome_two = Outcome("Corner", 2)
        outcome_three = Outcome("Black", 3)
        outcome_four = Outcome("Street", 4)

        nR = NonRandom()
        nR.setSeed(1)

        wheel_one = Wheel(nR)
        wheel_one.addOutcome(1, outcome_one)
        wheel_one.addOutcome(2, outcome_two)
        wheel_one.next()

        self.assertTrue(wheel_one.next(), outcome_one )

        #test getOutcome
        self.wheel_two = Wheel(nR)
        BB = BinBuilder()
        BB.buildBins(self.wheel_two)

class BinBuilderTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_BinBuilder(self):

        nR = NonRandom()
        nR.setSeed(1)

        wheel_one = Wheel(nR)

        BB = BinBuilder()
        BB.buildBins(wheel_one)

        ########### maybe delete since it isn't asked for
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

        #########

class BetTestCase(unittest.TestCase):

    def test_Bin(self):
        outcome_two = Outcome("Corner", 2)
        outcome_three = Outcome("Black", 3)

        bet1 = Bet(10, Outcome("Red", 1))
        bet2 = Bet(10, outcome_two)
        bet3 = Bet(10, outcome_three)

        self.assertTrue(bet1.winAmount() ==20,) # 10 + 10
        self.assertTrue(bet1.loseAmount() == 10) # lose of wager
        self.assertTrue(bet2.winAmount() == 30) #10*2 + 10
        self.assertTrue(bet2.loseAmount() == 10) # lose of wager
        self.assertTrue(bet3.winAmount() == 40) #10*3 + 10
        self.assertTrue(bet3.loseAmount() == 10) # lose of wager

        self.assertEqual(str(bet1), "amount on Red (1:1)")

class TableTestCase(unittest.TestCase):

    def test_Table(self):
        tbl = Table(limit=30)
        bet1 = Bet(10, Outcome("Red", 1))
        bet2 = Bet(20, Outcome("Corner", 2))
        bet3 = Bet(30, Outcome("Black", 3))
        bet4 = Bet(40, Outcome("Street", 4))

        self.assertTrue(tbl.isValid(bet1))
        self.assertTrue(tbl.isValid(bet3)) # a bet of 30 should be acceptable even with a limit of 30

        self.assertFalse(tbl.isValid(bet4)) # 40 should not be valid

        tbl.placeBet(bet1)
        tbl.placeBet(bet2)
        self.assertFalse(tbl.isValid(bet1))

        #test that exception will raise if a bet causes bets to exceed the table limit
        # http://www.lengrand.fr/2011/12/pythonunittest-assertraises-raises-error/
        self.assertRaises(InvalidBet, lambda: tbl.placeBet(bet2)) # this should raise an exception

        # test that Table object is iterable
        self.assertTrue(isinstance(tbl, collections.Iterable))

    def test_TableStr(self):
        tbl = Table(limit=30)
        tbl.placeBet(Bet(10, Outcome("Red", 1)))
        self.assertEquals(str(tbl), "['amount on Red (1:1)']")

class GameTestCase(unittest.TestCase):
    """
    This runs the game a few times for testing
    """
    def test_game(self):
        log = logging.getLogger( "GameTestCase.test_game" )

        # make wheel
        self.nR = NonRandom()
        self.nR.setSeed(2)
        self.wheel = Wheel(self.nR)
        # make BinBuilder and build bins for wheel
        bin_builder = BinBuilder()
        bin_builder.buildBins(self.wheel)
        # make table
        table = Table(limit=100)
        # make player
        _p57 = Passenger57(table=table, stake=100, roundsToGo=100)
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
        self.nR = NonRandom()
        self.nR.setSeed(1) # red
        wheel = Wheel(self.nR)
        self.table = Table(limit=100)
        bin_builder = BinBuilder()
        bin_builder.buildBins(wheel)
        self.game = RouletteGame(wheel, self.table)

class GameBlack(unittest.TestCase):
    def setUp(self):
        # wheel -- returns bin 2
        self.nR = NonRandom()
        self.nR.setSeed(2) # black
        wheel = Wheel(self.nR)
        self.table = Table(limit=100)
        bin_builder = BinBuilder()
        bin_builder.buildBins(wheel)
        self.game = RouletteGame(wheel, self.table)

class MartingaleTestBlack(GameBlack):
    """
    Black wins every time
    """
    def test_black(self):
        _martin = Martingale(table=self.table, stake=100, roundsToGo=10)
        for i in range(4):
            self.game.cycle(_martin)

        self.assertEqual(_martin.stake, 104)

        #test setStake and setRounds
        _martin.setStake(200)
        self.assertEqual(_martin.stake, 200)
        _martin.setRounds(20)
        self.assertEqual(_martin.roundsToGo, 20)

class MartingaleTestRed(GameRed):
    """
    Red looses every time
    """
    def test_Red(self):

        _martin = Martingale(table=self.table, stake=100, roundsToGo=10)
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
        
        _martin = Martingale(table=self.table, stake=100, roundsToGo=100)
        sim = Simulator(self.game, _martin)
        self.assertEqual(sim.session()[0:7], [99,97,93,85,69,37,0])

    def test_simulator_gather(self):
        _martin = Martingale(table=self.table, stake=100, roundsToGo=50)
        sim = Simulator(self.game, _martin)
        sim.gather()
        self.assertEqual(sim.duration, list( 7 for d in range(50)))

    def test_simulator_standard_deviation(self):
        _martin = Martingale(table=self.table, stake=100, roundsToGo=100)
        sim = Simulator(self.game, _martin)
        self.assertEqual(sim.standard_deviation([2,4,4,4,5,5,7,9]), 2)

class SimulatorP57Black(GameBlack):
    def test_p57_session(self):
        _p57 = Passenger57(table=self.table, stake=100, roundsToGo=100)
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
        _SR = SevenReds(table=self.table, stake=100, roundsToGo=100)

        for i in range(76):

            seed = seq.pop(0)
            self.nR.setSeed(seed)
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