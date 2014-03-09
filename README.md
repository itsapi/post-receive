post-receive
================

These scripts are run after code is pushed to the server. They compile everything and deploy to the correct location.

Each repository will have an individual `post-receive` file which checks out the files to a processing directory.

`main.py` is run in this directory, processing files as specified in `options.json`. The files are then transferred to the output directory.