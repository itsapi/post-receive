import os
import unittest
import main as pr


def diff(expected, actual):
    return os.system('diff -rq {} {}'.format(expected, actual))


class ProcessingTests(unittest.TestCase):

    def test_copy(self):
        pr.process(['tests/fixtures/copy'])
        self.assertFalse(diff('tests/expected/copy', 'tests/output/copy'))


if __name__ == '__main__':
    unittest.main()
