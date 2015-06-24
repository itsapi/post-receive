import os
import unittest
import main as pr


def diff(expected, actual):
    return os.system('diff -rq {} {}'.format(expected, actual))


def setup(name):
    os.system('mkdir -p tests/fixtures/processing')
    os.system('rm -r tests/fixtures/processing/*')
    os.system('cp -r tests/fixtures/input/* tests/fixtures/processing/')
    os.system('cp tests/fixtures/{}.json tests/fixtures/processing/options.json'.format(name))


class OptionsTests(unittest.TestCase):

    def test_build_cmd(self):
        setup('build_cmd')
        self.assertFalse(pr.process(['tests/fixtures/processing']))
        self.assertFalse(diff('tests/expected/build_cmd', 'tests/output/build_cmd'))

    def test_copy_from(self):
        setup('copy_from')
        self.assertFalse(pr.process(['tests/fixtures/processing']))
        self.assertFalse(diff('tests/expected/copy_from', 'tests/output/copy_from'))

    def test_copy_to(self):
        setup('copy_to')
        self.assertFalse(pr.process(['tests/fixtures/processing']))
        self.assertFalse(diff('tests/expected/copy_to', 'tests/output/copy_to'))

    def test_start_cmd(self):
        setup('start_cmd')
        self.assertFalse(pr.process(['tests/fixtures/processing']))
        self.assertFalse(diff('tests/expected/start_cmd', 'tests/output/start_cmd'))

    def test_ignore(self):
        setup('ignore')
        self.assertFalse(pr.process(['tests/fixtures/processing']))
        self.assertFalse(diff('tests/expected/ignore', 'tests/output/ignore'))


class FailureTests(unittest.TestCase):

    def test_no_copy_to(self):
        setup('no_copy_to')
        with self.assertRaises(SystemExit) as cm:
            pr.process(['tests/fixtures/processing'])
        self.assertEqual(cm.exception.code, 'post-receive [error]: no output directory specified in options.json')

    def test_build_cmd_failed(self):
        setup('build_cmd_failed')
        with self.assertRaises(SystemExit) as cm:
            pr.process(['tests/fixtures/processing'])
        self.assertEqual(cm.exception.code, 'post-receive [error]: exit 1 failed')

    def test_start_cmd_failed(self):
        setup('start_cmd_failed')
        with self.assertRaises(SystemExit) as cm:
            pr.process(['tests/fixtures/processing'])
        self.assertEqual(cm.exception.code, 'post-receive [error]: exit 1 failed')
        self.assertFalse(diff('tests/expected/start_cmd_failed', 'tests/output/start_cmd_failed'))


if __name__ == '__main__':
    unittest.main()
