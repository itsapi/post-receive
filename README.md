Post Receive
============

[![NPM Version](https://img.shields.io/npm/v/post-receive.svg)](https://www.npmjs.com/package/post-receive)
[![Build Status](https://img.shields.io/travis/itsapi/post-receive/master.svg)](https://travis-ci.org/itsapi/post-receive)
[![Dependency Status](https://img.shields.io/david/itsapi/post-receive.svg)](https://david-dm.org/itsapi/post-receive)

These scripts are run after code is pushed to the server. They compile everything and deploy to the correct location.

[github-listener](http://github.com/itsapi/github-listener) runs this script for each repository after fetching the files from Github.

`index.js` is run in this directory, processing files as specified in `options.json`. The files are then transferred to the output directory.

The `options.json` takes a number of different options for build steps:

- `build_cmd`:  `list`,   a list of shell commands to be run in repository root at processing stage
- `copy_from`:  `string`, copy the contents of this directory to the output directory
- `copy_to`:    `string`, the directory files should be copied to after processing
- `start_cmd`: `list`,   a list of shell commands to be run in output directory after processing
- `ignore`:     `list`,   a list of files and directories in the output directory that should not be overwritten/deleted
- `url`:        `string`, a link to be displayed after processing on the github listener output
- `email`:      `list`,   a list of email addresses to send error messages if the build fails
