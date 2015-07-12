var os = require('os');
var fs = require('fs');
var exec = require('child_process').execSync;
var format = require('string-format');
var nodemailer = require('nodemailer');


var transporter = nodemailer.createTransport();
format.extend(String.prototype);


function run_cmd(cmd) {
  try {
    exec(cmd);
  } catch (e) {
    return true;
  }
}


var PostReceive = function(options) {
  var self = this;

  options = options || {};

  self.wk_path = options.cwd;
  self.logging = options.logging;
  self.options = options.config;

  self.load_options();
};

PostReceive.prototype.process = function() {
  var self = this;

  self.orig_cwd = process.cwd();
  process.chdir(self.wk_path);

  if (self.options.build_cmd) {
    self.run_commands(self.options.build_cmd);
  }

  if (self.options.copy_to) {
    run_cmd('mkdir -p ' + self.options.copy_to);

    self.options.ignore = (self.options.ignore || []).concat(['options.json', 'node_modules']);

    self.clear_dir();
    self.move_files();
    process.chdir(self.options.copy_to);

    if (self.options.start_cmd) {
      self.run_commands(self.options.start_cmd);
    }

  } else {
    self.error('no output directory specified in options.json');
  }

  self.log('finished');
  process.chdir(self.orig_cwd);

  if (self.options.url) {
    self.log('site should now be live at ' + self.options.url);
  }
};

PostReceive.prototype.log = function(message) {
  if (this.logging) {
    console.log('post-receive:', message);
  }
};

PostReceive.prototype.load_options = function() {
  var self = this;

  for (var option in (self.options.hosts && self.options.hosts[os.hostname()])) {
    self.options[option] = self.options.hosts[os.hostname()][option];
  }
};

PostReceive.prototype.run_commands = function(commands) {
  var self = this;

  commands.forEach(function(cmd) {
    self.log('running "{}"'.format(cmd));

    if (run_cmd(cmd)) {
      self.error('{} failed'.format(cmd));
    }
  });
};

PostReceive.prototype.clear_dir = function() {
  var self = this;

  var wk_path = process.cwd();
  var directory = self.options.copy_to;
  var patterns = self.options.ignore;

  process.chdir(directory);

  self.log('removing files from ' + directory);
  patterns = patterns.map(function(p) {
    return fs.existsSync(p) && fs.lstatSync(p).isDirectory() ? p + '/*' : p;
  });

  var d = "' ! -path './";
  var cmd = "find . ! -path './{}' -delete".format(patterns.join(d));

  run_cmd(cmd);
  process.chdir(wk_path);
};

PostReceive.prototype.move_files = function() {
  var self = this;

  var copy_from = self.options.copy_from;
  var copy_to = self.options.copy_to;
  var patterns = self.options.ignore;

  self.log('copying files to ' + copy_to);

  var cmd = 'rsync -r --exclude="{pattern}" {input}/. {out}'.format({
    pattern: patterns.join('" --exclude="'),
    input: copy_from || '.',
    out: copy_to
  });

  run_cmd(cmd);
};

PostReceive.prototype.error = function(message) {
  var self = this;

  var name = self.wk_path;

  if (self.options.email) {
    var subject = name + ' build failed';
    var body = '{} failed to build correctly at {}\nError message: {}'
                .format(name, Date.toString(), message);

    transporter.sendMail({
      to: self.options.email,
      subject: subject,
      text: body
    });
  }

  process.chdir(self.orig_cwd);
  throw('post-receive [error]: ' + message);
};


module.exports = PostReceive;
