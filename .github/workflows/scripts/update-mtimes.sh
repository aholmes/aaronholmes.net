#!/bin/sh -e

# https://gist.github.com/HackingGate/9e8169c7645b074b2f40c959ca20d738

OS=${OS:-`uname`}

if [ "$OS" = 'Darwin' ]; then
  get_touch_time() {
    date -r ${unixtime} +'%Y%m%d%H%M.%S'
  }
else
  # default Linux
  get_touch_time() {
    date -d @${unixtime} +'%Y%m%d%H%M.%S'
  }
fi

# all git files
git ls-tree -r --name-only HEAD source/**/*.rst > .git_ls-tree_r_name-only_HEAD

# minus https://stackoverflow.com/questions/1370996/minus-operation-on-two-files-using-linux-commands

# only restore files not modified
cat .git_ls-tree_r_name-only_HEAD | while read filename; do
  unixtime=$(git log -1 --format="%at" -- "${filename}")
  touchtime=$(get_touch_time)
  echo ${touchtime} "${filename}"
  touch -t ${touchtime} "${filename}"
done

rm .git_ls-tree_r_name-only_HEAD
