#!/bin/bash

url="$1"
name=${url##*/}
path="/home/git/post-receive/processing"

mkdir $path
shopt -s extglob
rm -rf $path/!(node_modules)

if [ ! -d "/home/git/$name.git" ]; then
  echo hi
  cd /home/git
  git clone --bare $url
fi
cd /home/git/$name.git

git fetch $url master:master -f
export GIT_WORK_TREE=$path
git checkout -f

cd $path

python3 ../main.py "$name"
