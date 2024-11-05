import unittest


def freeze_check(method):

    def wrapper(self, *args, **kwargs):
        if self.is_frozen:
            self.skipTest('Тесты в этом кейсе заморожены')
        return method(self, *args, **kwargs)

    return wrapper


class RunnerTest(unittest.TestCase):
    is_frozen = False

    @freeze_check
    def test_challenge(self):
        self.assertEqual(1 + 1, 2)

    @freeze_check
    def test_run(self):
        self.assertTrue(True)

    @freeze_check
    def test_walk(self):
        self.assertFalse(False)


class TournamentTest(unittest.TestCase):
    is_frozen = True

    @freeze_check
    def test_first_tournament(self):
        self.assertEqual(2 * 2, 4)

    @freeze_check
    def test_second_tournament(self):
        self.assertEqual(3 - 1, 2)

    @freeze_check
    def test_third_tournament(self):
        self.assertEqual(5 + 5, 10)