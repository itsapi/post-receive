var test = require('tape');
var common = require('./common');


test('no_copy_to', function(t) {
  common.setup('no_copy_to');
  var pr = common.create_pr();

  t.throws(function() {
    pr.process();
  }, 'post-receive throws an exception');

  t.end();
});

test('build_cmd_failed', function(t) {
  common.setup('build_cmd_failed');
  var pr = common.create_pr();

  t.throws(function() {
    pr.process();
  }, 'post-receive throws an exception');

  t.end();
});

test('start_cmd_failed', function(t) {
  common.setup('start_cmd_failed');
  var pr = common.create_pr();

  t.throws(function() {
    pr.process();
  }, 'post-receive throws an exception');

  t.notok(common.diff('tests/expected/start_cmd_failed', 'tests/output/start_cmd_failed'), 'output directory is as expected');
  t.end();
});
