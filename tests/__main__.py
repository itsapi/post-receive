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


class FailureTests(unittest.TestCase):

    def test_no_copy_to(self):
        with self.assertRaises(SystemExit) as cm:
            pr.process(['tests/fixtures/no_copy_to'])
        self.assertEqual(cm.exception.code, 'post-receive [error]: no output directory specified in options.json')

    def test_build_cmd_failed(self):
        with self.assertRaises(SystemExit) as cm:
            pr.process(['tests/fixtures/build_cmd_failed'])
        self.assertEqual(cm.exception.code, 'post-receive [error]: exit 1 failed')

    def test_start_cmd_failed(self):
        with self.assertRaises(SystemExit) as cm:
            pr.process(['tests/fixtures/start_cmd_failed'])
        self.assertEqual(cm.exception.code, 'post-receive [error]: exit 1 failed')
        self.assertFalse(diff('tests/expected/start_cmd_failed', 'tests/output/start_cmd_failed'))


if __name__ == '__main__':
    unittest.main()
