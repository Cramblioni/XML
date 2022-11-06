
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

class MagicFunc:
  __slots__ = ("func",)
  def __init__(self,func): self.func = func
class PassFunc:
  __slots__ = ("func",)
  def __init__(self,func): self.func = func
  def __repr__(self): return f"<passed {self.func.__name__}>"

def _wrap(env):
  return noArg(map(setret, env.maps))

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
        tmp = solve(i, _wrap(env))
      return tmp
    case [Ident("local"), Ident(var), val, *_]:
      env[var] = solve(val, _wrap(env))
    case [fnc, *args]:
      func = solve(fnc, _wrap(env))
      if isinstance(func, PassFunc):
        return func.func(*map(solve, args, map(_wrap, repeat(env))))
      if isinstance(func, MagicFunc):
        return func.func(env, args)
      assert False, "Not Implemented"
    case [fnc]:
      return solve(fnc, _wrap(env))

def XMLlist(*args):
  return list(args)

def XMLmap(func, *itrs):
  out = []
  for args in zip(*itrs):
    out.append(func.func(*args))
  return out

def util_XMLimport(package):
  def wrap(x): return PassFunc(x) if callable(x) else x
  return {
    attr : wrap(getattr(package, attr))
    for attr in filter(lambda x: not x.startswith("_"), dir(package))
  }

def XMLimport(env, args):
  assert len(args) > 0
  assert isinstance(args[0], Ident)

  if args[0].name == "external":
    assert len(args) > 1
    assert isinstance(args[1], Ident)
    venv = {}
    exec(f"import {args[1].name} as implib", venv)
    env.update(util_XMLimport(venv["implib"]))
  else:
    assert False, "Importing xml scripts not implemented"


def prelude():
  import operator
  prelude = {
    "print": PassFunc(print),
    "list": PassFunc(XMLlist),
    "map": PassFunc(XMLmap),
    "import": MagicFunc(XMLimport),
    "range": PassFunc(range),
    "setattr": PassFunc(setattr),
    "getattr": PassFunc(getattr),
    **util_XMLimport(operator)
  }
  return noArg(map(setret, [prelude, {}]))

if __name__ == "__main__":
  # this should print 5.0 and return `"party"`
  
  x = solve(parse("test.xml"), prelude())
  print("Result ::", x)
