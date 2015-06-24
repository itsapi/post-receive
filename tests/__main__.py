import os
import unittest
import main as pr


def diff(expected, actual):
    return os.system('diff -rq {} {}'.format(expected, actual))


class ProcessingTests(unittest.TestCase):

    def test_copy_to(self):
        pr.process(['tests/fixtures/copy_to'])
        self.assertFalse(diff('tests/expected/copy_to', 'tests/output/copy_to'))

    def test_copy_from(self):
        pr.process(['tests/fixtures/copy_from'])
        self.assertFalse(diff('tests/expected/copy_from', 'tests/output/copy_from'))

    def test_build_cmd(self):
        pr.process(['tests/fixtures/build_cmd'])
        self.assertFalse(diff('tests/expected/build_cmd', 'tests/output/build_cmd'))


if __name__ == '__main__':
    unittest.main()
