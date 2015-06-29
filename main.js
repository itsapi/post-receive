var os = require('os'),
    exec = require('child_process').execSync,
    format = require('string-format');

format.extend(String.prototype)


function PostReceive(options) {
  options = options || {};
  this.logging = options.logging;

  this.args = process.argv.slice(2);
  this.wk_path = args.shift() || process.cwd();
  this.name = args.shift() || this.wk_path;
}

PostReceive.prototype.process = function () {

  orig_cwd = process.cwd();
  process.chdir(this.wk_path);

  this.options = require('./options.json');
  this.load_options();

  if (this.options.build_cmd) {
    run_commands(this.options.build_cmd);
  }

  if (this.options.copy_to) {
    os.system('mkdir -p ' + this.options.copy_to)

    this.options.ignore = (this.options.ignore || []).concat(['options.json', 'node_modules'])

    clear_dir(copy_to, ignore)
    move_files(copy_from, copy_to, ignore)
    process.chdir(this.options.copy_to)

    if (this.options.start_cmd) {
      run_commands(this.options.start_cmd)
    }

  } else {
    this.error('no output directory specified in options.json')
  }

  this.log('finished')
  process.chdir(orig_cwd)

  if (this.options.url) {
    this.log('site should now be live at ' + this.options.url);
  }
};

PostReceive.prototype.log = function (message) {
  if (this.logging) {
    console.log('post-receive:', message);
  }
};

PostReceive.prototype.load_options = function () {
  for (var option in (this.options.hosts && this.options.hosts[os.hostname()])) {
    this.options[option] = this.options.hosts[os.hostname()][option];
  }
};

PostReceive.prototype.run_commands = function (commands) {
  var self = this;

  commands.forEach(function (cmd) {
    self.log('running "{}"'.format(cmd));

    exec(cmd, function (error, stdout, stderr) {
      if (error) {
        self.error('{} failed'.format(cmd));
      }
    });
  });
};


function clear_dir(directory, patterns) {
  var self = this;

  var wk_path = os.getcwd();
  process.chdir(directory);

  self.log('removing files from ' + directory);
  pattern = patterns.map(function (p) {
    return fs.lstatSync(p).isDirectory() ? p + '/*' : p;
  });

  var d = "' ! -path './";
  var cmd = "find . ! -path './{}' -delete".format(patterns.join(d));

  try {
    exec(cmd, function (error, stdout, stderr) {

    });
  } catch {

  }

  os.chdir(wk_path);
}


function move_files(copy_from, copy_to, patterns) {
  this.log('copying files to ' + copy_to)
  os.system('rsync -r --exclude="{pattern}" {input}/. {out}'
        .format(
          pattern=patterns.join('" --exclude="'),
          input=copy_from if copy_from else '.',
          out=copy_to
        )
        )
}


function error(name, email, error) {
  if (email) {
    var subject = name + ' build failed'
    var body = ('{} failed to build correctly at {}\nError message: {}'
                .format(name, time.strftime('%c'), error));

    var p = os.popen('mail -s "{}" {}'.format(subject, ' '.join(email)), 'w')
    p.write(body)
    p.close()
  }

  this.log('post-receive [error]: ' + error);
  process.exit(1);
}
