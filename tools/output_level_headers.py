#!/usr/bin/env python3

import sys

def main():
  if len(sys.argv) < 3:
    sys.stderr.write("Usage: %s input_file output_file")
    exit(1)

  input_filename = sys.argv[1]
  output_filename = sys.argv[2]

  with open(output_filename, "w") as output_file:
    with open(input_filename, "r") as input_file:
      line = input_file.readline()
      while line:
        line = line.strip()
        if line and line[0] != '#':
          output_file.write('#include "{}"\n'.format(line.strip()))
        line = input_file.readline()

if __name__ == "__main__":
    main()
