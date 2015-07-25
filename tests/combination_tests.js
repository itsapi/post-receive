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

test('combo_three', function(t) {
  t.test('hostname server1', function(st) {
    common.setup('combo_three');
    var pr = common.create_pr({hostname: 'server1'});
    st.notok(pr.process(), 'post-receive exits cleanly');
    st.notok(common.diff('tests/expected/combo_three_a', 'tests/output/combo_three'), 'output directory is as expected');
    st.end();
  });

  t.test('hostname server2', function(st) {
    common.setup('combo_three');
    var pr = common.create_pr({hostname: 'server2'});
    st.notok(pr.process(), 'post-receive exits cleanly');
    st.notok(common.diff('tests/expected/combo_three_b', 'tests/output/combo_three'), 'output directory is as expected');
    st.end();
  });
});
