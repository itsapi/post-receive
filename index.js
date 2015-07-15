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


/**
 * Creates a new `PostReceive` instance.
 * @name PostReceive
 * @function
 * @param {Object} options An object containing the following fields:
 *
 *  - `cwd` (String): The working directory to start processing in
 *  - `logging` (Boolean): Output logs if `true`
 *  - `config` (Object): The `options.json` to use for the build process (see example)
 */

var PostReceive = function(options) {
  var self = this;

  options = options || {};

  self.wk_path = options.cwd;
  self.logging = options.logging;
  self.options = options.config;

  self.load_options();
};

/**
 * Run the build process
 * @name PostReceive.process
 * @function
 */

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

/**
 * Log a message if `this.logging`
 * @name PostReceive.log
 * @function
 * @param {Anything} message Message to log to console
 */

PostReceive.prototype.log = function(message) {
  if (this.logging) {
    console.log('post-receive:', message);
  }
};

/**
 * Parse `this.options` to load host specific options
 * @name PostReceive.load_options
 * @function
 */

PostReceive.prototype.load_options = function() {
  var self = this;

  for (var option in (self.options.hosts && self.options.hosts[os.hostname()])) {
    self.options[option] = self.options.hosts[os.hostname()][option];
  }
};

/**
 * Run list of shell commands sequentially, handling errors
 * @name PostReceive.run_commands
 * @function
 * @param {Array} commands List of commands to run
 */

PostReceive.prototype.run_commands = function(commands) {
  var self = this;

  commands.forEach(function(cmd) {
    self.log('running "{}"'.format(cmd));

    if (run_cmd(cmd)) {
      self.error('{} failed'.format(cmd));
    }
  });
};

/**
 * Empty the `copy_to` directory, excluding paths in ignore list
 * @name PostReceive.clear_dir
 * @function
 */

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

/**
 * Copy processed files to `copy_to` directory, excluding paths in ignore list
 * @name PostReceive.move_files
 * @function
 */

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

/**
 * Handle build error
 * @name PostReceive.error
 * @function
 * @param {String} message Error message to be logged and sent in build failed email
 */

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
