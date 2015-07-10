var test = require('tape');
var common = require('./common');


test('build_cmd', function(t) {
  common.setup('build_cmd');
  var pr = common.create_pr();
  t.notok(pr.process(['fixtures/processing']));
  t.notok(common.diff('tests/expected/build_cmd', 'tests/output/build_cmd'));
  t.end();
});

test('copy_from', function(t) {
  common.setup('copy_from');
  var pr = common.create_pr();
  t.notok(pr.process(['fixtures/processing']));
  t.notok(common.diff('tests/expected/copy_from', 'tests/output/copy_from'));
  t.end();
});

test('copy_to', function(t) {
  common.setup('copy_to');
  var pr = common.create_pr();
  t.notok(pr.process(['fixtures/processing']));
  t.notok(common.diff('tests/expected/copy_to', 'tests/output/copy_to'));
  t.end();
});

test('start_cmd', function(t) {
  common.setup('start_cmd');
  var pr = common.create_pr();
  t.notok(pr.process(['fixtures/processing']));
  t.notok(common.diff('tests/expected/start_cmd', 'tests/output/start_cmd'));
  t.end();
});

test('ignore', function(t) {
  common.setup('ignore');
  var pr = common.create_pr();
  t.notok(pr.process(['fixtures/processing']));
  t.notok(common.diff('tests/expected/ignore', 'tests/output/ignore'));
  t.end();
});
