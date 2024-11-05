import unittest
import logging
from rt_with_exceptions import Runner

logging.basicConfig(
    level=logging.INFO,
    filename='runner_tests.log',
    filemode='w',
    encoding='UTF-8',
    format='%(levelname)s: %(message)s'
)


class RunnerTest(unittest.TestCase):
    def test_walk(self):
        try:
            r1 = Runner("Вася", -5)
            logging.info('"test_walk" выполнен успешно')
        except ValueError as e:
            logging.warning("Неверная скорость для Runner")
            self.assertTrue(isinstance(e, ValueError))

    def test_run(self):
        try:
            r2 = Runner(2)
            logging.info('"test_run" выполнен успешно')
        except TypeError as e:
            logging.warning("Неверный тип данных для объекта Runner")
            self.assertTrue(isinstance(e, TypeError))


if __name__ == "__main__":
    unittest.main()
