
# name idea "XML - XML May-be Lisp
import ast
from iters import *
from xml.etree import ElementTree
from collections import ChainMap

class Ident:
  __slots__ = ("name",)
  __match_args__ = ("name",)
  def __init__(self, name): self.name = name
  def __repr__(self): return f"Ident({self.name!r})"
  def __hash__(self): return hash(self.name)
  def __eq__(self, oth): return isinstance(oth, Ident) and self.name is oth.name

class SexprList(list): pass

def parse(path): # just rejigging
  result = []
  stack  = [result]
  
  for (evnt, elem) in ElementTree.iterparse(path, ("start", "end")):
    if evnt == "start":
      cur = SexprList((Ident(elem.tag),))
      stack.append(cur)
    elif evnt == "end":
      cur = stack.pop()
      if elem.tag in ("lit", "literal"):
        assert len(elem.findall("./*")) == 0, "literal cannot have children"
        cur[0] = ast.literal_eval(elem.text)
      if len(cur) == 1:
        stack[-1].extend(cur)
      else:
        stack[-1].append(cur)
    else:
      assert False, f"Cannot handle event \"{evnt}\""

  [result] = result
  return result

class FuncMagic:
  __slots__ = ("func",)
  def __init__(self,func): self.func = func
class PassFunc:
  __slots__ = ("func",)
  def __init__(self,func): self.func = func


def solve(prog, varTable=noArg([dict])):
  # if a function is `magic` pass the entire expression
  # otherwise evaluate and hand over
  # this function **MUST** return whatever the program
  # returns

  # varTable is a factory function which returns `Iterable[Dict]`
  env = ChainMap(*varTable)
  if isinstance(prog, Ident): return env[prog.name]
  elif not isinstance(prog, SexprList): return prog
  match prog:
    case [Ident("block"), *args]:
      tmp = None
      for i in args:
        tmp = solve(i, noArg([setret(env)]))
      return tmp
    case [Ident("local"), Ident(var), val, *_]:
      env[var] = solve(val,noArg([setret(env)]))
    case [fnc, *args]:
      func = solve(fnc, noArg([setret(env)]))
      if isinstance(func, PassFunc):
        return func.func(*map(solve, args, repeat(noArg([setret(env)]))))
      assert False, "Not Implemented"
    case [fnc]:
      return solve(fnc,noArg([setret(env)]))

if __name__ == "__main__":
  # this should print 5.0 and return `"party"`
  x = solve(parse("test.xml"), noArg([setret({"print":PassFunc(print)})]))
  print("Result ::", x)
