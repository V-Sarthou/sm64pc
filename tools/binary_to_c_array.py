#!/usr/bin/env python3

import sys
import os
import subprocess
import binascii

def main():
  if len(sys.argv) < 3:
    sys.stderr.write("Usage: %s binary_file variable_name")
    exit(1)

  input_filename = sys.argv[1]
  var_name = sys.argv[2]

  output_c_filename = "%s.c" % input_filename

  with open(output_c_filename, "w") as output_file:
    output_file.write("unsigned char %s[] = {\n  " % var_name)
    with open(input_filename, "rb") as input_file:
      hexstr = binascii.hexlify(input_file.read()).decode("UTF-8")
      output_file.write(", ".join(["0x" + hexstr[i:i + 2] for i in range(0, len(hexstr), 2)]))
    output_file.write("\n};\n")

if __name__ == "__main__":
    main()
