Post Receive
============

These scripts are run after code is pushed to the server. They compile everything and deploy to the correct location.

[github-listener](http://github.com/itsapi/github-listener) runs this script for each repository after fetching the files from Github.

`main.py` is run in this directory, processing files as specified in `options.json`. The files are then transferred to the output directory.

The `options.json` takes a number of different options for build steps:

- `output`:    `string`, the directory files should be copied to after processing
- `build_dir`: `string`, copy the contents of this directory to the output directory
- `ignore`:    `list`,   a list of files and directories in the output directory that should not be overwritten/deleted
- `grunt`:     `bool`,   should grunt be run during processing?
- `node`:      `bool`,   should npm install be run in the output directory?
- `build_cmd`: `string`, a shell command to be run in repository root at processing stage
- `command`:   `string`, a shell command to be run in output directory after processing
- `url`:       `string`, a link to be displayed after processing on the github listener output
- `email`:     `list`,   a list of email addresses to send error messages if the build fails
