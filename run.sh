#!/bin/bash

url="$1"
name=${url##*/}
path="/home/git/post-receive/processing"

shopt -s extglob
rm -rf $path/!(node_modules)

cd /home/git/$name.git

git fetch $url master:master
export GIT_WORK_TREE=$path
git checkout -f

cd $path

python3 ../main.py
