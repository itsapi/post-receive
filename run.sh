#!/bin/bash

path="/home/git/post-receive/processing"

shopt -s extglob
rm -rf $path/!(node_modules)

export GIT_WORK_TREE=$path
git checkout -f

cd $path

python3 ../main.py
