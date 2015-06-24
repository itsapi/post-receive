import os
import unittest
import main as pr


def diff(expected, actual):
    return os.system('diff -rq {} {}'.format(expected, actual))


class OptionsTests(unittest.TestCase):

    def test_build_cmd(self):
        self.assertFalse(pr.process(['tests/fixtures/build_cmd']))
        self.assertFalse(diff('tests/expected/build_cmd', 'tests/output/build_cmd'))

    def test_copy_from(self):
        self.assertFalse(pr.process(['tests/fixtures/copy_from']))
        self.assertFalse(diff('tests/expected/copy_from', 'tests/output/copy_from'))

    def test_copy_to(self):
        self.assertFalse(pr.process(['tests/fixtures/copy_to']))
        self.assertFalse(diff('tests/expected/copy_to', 'tests/output/copy_to'))

    def test_start_cmd(self):
        self.assertFalse(pr.process(['tests/fixtures/start_cmd']))
        self.assertFalse(diff('tests/expected/start_cmd', 'tests/output/start_cmd'))

    def test_ignore(self):
        self.assertFalse(pr.process(['tests/fixtures/ignore']))
        self.assertFalse(diff('tests/expected/ignore', 'tests/output/ignore'))


if __name__ == '__main__':
    unittest.main()
