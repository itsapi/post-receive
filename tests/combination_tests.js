var test = require('tape');
var common = require('./common');


test('combo_one', function(t) {
  common.setup('combo_one');
  var pr = common.create_pr();
  t.notok(pr.process(), 'post-receive exits cleanly');
  t.notok(common.diff('tests/expected/combo_one', 'tests/output/combo_one'), 'output directory is as expected');
  t.end();
});

test('combo_two', function(t) {
  common.setup('combo_two');
  var pr = common.create_pr();
  t.notok(pr.process(), 'post-receive exits cleanly');
  t.notok(common.diff('tests/expected/combo_two', 'tests/output/combo_two'), 'output directory is as expected');
  t.end();
});
