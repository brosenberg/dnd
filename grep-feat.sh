#!/bin/bash
FEAT_DB=~/Downloads/Feats.tsv
grep -i "$1" $FEAT_DB | awk -F'\t' '{print "[1;33m" $2 "[0m: " $4}' | sed "s/$1/[1;31m&[0m/gi"
