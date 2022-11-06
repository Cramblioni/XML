
# the xmli script.
# no promises made on error handling

import core
import sys

if not __name__ == "__main__":
  print("Not Importable")
else:
  if len(sys.argv) <= 1:
    print("please provide script path", file=sys.stderr)
  else:
    code = core.parse(sys.argv[1])
    print(">>", core.solve(code, core.prelude()))
