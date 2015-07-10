var exec = require('child_process').spawnSync;
var format = require('string-format');
var PostReceive = require('../');


format.extend(String.prototype);


var common = {};

common.diff = function(expected, actual) {
  return exec('diff', ['-rq', expected, actual]).status;
};

common.setup = function(name) {
  exec('mkdir', ['-p', 'tests/fixtures/processing']);
  exec('rm', ['-r', 'tests/fixtures/processing/.']);
  exec('cp', ['-r', 'tests/fixtures/input/.', 'tests/fixtures/processing/']);
  exec('cp', ['tests/fixtures/{}.json'.format(name), 'tests/fixtures/processing/options.json']);
};

common.create_pr = function() {
  var options = {};

  options.config = require('./fixtures/processing/options.json');
  options.cwd = 'tests/fixtures/processing';
  options.logging = true;

  return new PostReceive(options);
};

module.exports = common;
