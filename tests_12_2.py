import unittest
from runner_and_tournament import Runner, Tournament


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner("Усэйн", speed=10)
        self.andrei = Runner("Андрей", speed=9)
        self.nick = Runner("Ник", speed=3)

    @classmethod
    def tearDownClass(cls):
        for key, result in cls.all_results.items():
            print(result)

    def test_race_usain_nick(self):
        race = Tournament(90, self.usain, self.nick)
        result = race.start()

        self.all_results[1] = {place: str(runner) for place, runner in result.items()}

        self.assertTrue(str(result[max(result.keys())]) == "Ник")

    def test_race_andrei_nick(self):
        race = Tournament(90, self.andrei, self.nick)
        result = race.start()

        self.all_results[2] = {place: str(runner) for place, runner in result.items()}

        self.assertTrue(str(result[max(result.keys())]) == "Ник")

    def test_race_usain_andrei_nick(self):
        race = Tournament(90, self.usain, self.andrei, self.nick)
        result = race.start()

        self.all_results[3] = {place: str(runner) for place, runner in result.items()}

        self.assertTrue(str(result[max(result.keys())]) == "Ник")


if __name__ == '__main__':
    unittest.main()
