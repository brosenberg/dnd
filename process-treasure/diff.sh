#!/bin/bash

if [ -z "$1" ]; then
    COMMIT="HEAD~1"
else
    COMMIT=$1
fi
diff_out=$(mktemp /tmp/diff.XXXXX)
git diff $COMMIT $treasure > $diff_out

old=$(sed '/^+/d' $diff_out | ./process-treasure.pl | sed -r '$!d;s/^\S+\s+(\S+)\s.*$/\1/')
new=$(sed '/^-/d' $diff_out | ./process-treasure.pl | sed -r '$!d;s/^\S+\s+(\S+)\s.*$/\1/')

echo "$new - $old"
diff=$(bc -l <<< "$new - $old")
echo "Gained $diff gp"

rm $diff_out
