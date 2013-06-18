#!/bin/bash

function usedit {
    echo -e "\t\"$name\":{"
    (for i in *$file*; do 
        sed '/^#/d;s/^/		"/;s/$/":1,/' $i
    done) | sed '$s/,$//'
    echo -en "\t}"
}

echo "{"
name="Surname"
file='-last'
usedit
echo ,
name="Male First Name"
file='-male'
usedit
echo ,
name="Female First Name"
file='female'
usedit
echo -e "\n}"
