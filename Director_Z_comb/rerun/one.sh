#!/bin/bash
# args: name relpath deps(comma or -) args...
R=/tmp/claude-0/-home-user/1b3e59a6-be8f-5e36-be7c-26b1885eea91/scratchpad/comb/rerun
name=$1; rel=$2; deps=$3; shift 3
d=$R/run/$name; rm -rf $d; mkdir -p $d; cp $R/src/$rel $d/
if [ "$deps" != "-" ]; then for f in ${deps//,/ }; do cp $R/src/$f $d/; done; fi
cd $d; ls > .before
s=$(date +%s.%N)
timeout 240 python3 $(basename $rel) "$@" > stdout.log 2> stderr.log
ec=$?
e=$(date +%s.%N)
new=$(ls | grep -vxFf .before | grep -v -e stdout.log -e stderr.log -e __pycache__ | tr '\n' ' ')
printf "%s|%s|%.1f|%s|%s\n" "$name" "$ec" "$(echo "$e - $s" | bc)" "$new" "$(tail -1 stderr.log | cut -c1-200)" >> $R/status.txt
