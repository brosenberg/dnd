#!/usr/bin/env python

import argparse
import json

def main():
    #p = argparse.ArgumentParser()
    #p.add_argument('-f', '--file', type=str, help='Input file')
    #args = p.parse_args()
    base = {}
    with open('base.json', 'r') as f:
        base = json.load(f)
    print base 

if __name__ == '__main__':
    main()
