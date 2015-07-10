#!/usr/bin/env node

var os = require('os');
var exec = require('child_process').execSync;
var format = require('string-format');
var nodemailer = require('nodemailer');


var transporter = nodemailer.createTransport();
format.extend(String.prototype);


function PostReceive(options) {
  options = options || {};
  this.logging = options.logging;

  this.args = process.argv.slice(2);
  this.wk_path = args.shift() || process.cwd();
  this.name = args.shift() || this.wk_path;
}

PostReceive.prototype.process = function() {
  var self = this;

  orig_cwd = process.cwd();
  process.chdir(self.wk_path);

  self.options = require('./options.json');
  self.load_options();

  if (self.options.build_cmd) {
    run_commands(self.options.build_cmd);
  }

  if (self.options.copy_to) {
    exec('mkdir -p ' + self.options.copy_to);

    self.options.ignore = (self.options.ignore || []).concat(['options.json', 'node_modules']);

    clear_dir(copy_to, ignore);
    move_files(copy_from, copy_to, ignore);
    process.chdir(self.options.copy_to);

    if (self.options.start_cmd) {
      run_commands(self.options.start_cmd);
    }

  } else {
    self.error('no output directory specified in options.json');
  }

  self.log('finished');
  process.chdir(orig_cwd);

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
  for (var option in (this.options.hosts && this.options.hosts[os.hostname()])) {
    this.options[option] = this.options.hosts[os.hostname()][option];
  }
};

PostReceive.prototype.run_commands = function(commands) {
  var self = this;

  commands.forEach(function(cmd) {
    self.log('running "{}"'.format(cmd));

    exec(cmd, function(error, stdout, stderr) {
      if (error) {
        self.error('{} failed'.format(cmd));
      }
    });
  });
};


PostReceive.prototype.clear_dir = function(directory, patterns) {
  var self = this;

  var wk_path = os.getcwd();
  process.chdir(directory);

  self.log('removing files from ' + directory);
  pattern = patterns.map(function(p) {
    return fs.lstatSync(p).isDirectory() ? p + '/*' : p;
  });

  var d = "' ! -path './";
  var cmd = "find . ! -path './{}' -delete".format(patterns.join(d));

  exec(cmd);
  os.chdir(wk_path);
};


PostReceive.prototype.move_files = function(copy_from, copy_to, patterns) {
  this.log('copying files to ' + copy_to);

  var cmd = 'rsync -r --exclude="{pattern}" {input}/. {out}'.format({
    pattern: patterns.join('" --exclude="'),
    input: copy_from || '.',
    out: copy_to
  });

  exec(cmd);
};


PostReceive.prototype.error = function(message) {
  var self = this;

  if (self.options.email) {
    var subject = name + ' build failed';
    var body = '{} failed to build correctly at {}\nError message: {}'
                .format(self.name, Date.toString(), message);

    transporter.sendMail({
      to: self.options.email,
      subject: message,
      text: body
    });
  }

  this.log('post-receive [error]: ' + message);
  process.exit(1);
};
