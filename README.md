Post Receive
============

These scripts are run after code is pushed to the server. They compile everything and deploy to the correct location.

[github-listener](http://github.com/itsapi/github-listener) runs this script for each repository after fetching the files from Github.

`main.py` is run in this directory, processing files as specified in `options.json`. The files are then transferred to the output directory.
