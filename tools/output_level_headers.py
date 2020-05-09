#!/usr/bin/env python3
import sys
for line in sys.stdin:
    line = line.strip()
    if line and line[0] != '#':
        print('#include "{}"'.format(line.strip()))
