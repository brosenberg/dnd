#!/usr/bin/env python3

import json
import random

surges = json.load(open('surges.json'))

print(random.choice(surges))
