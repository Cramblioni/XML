# XML
### Xml May-be Lisp

XML esque programming language. The acronym isn't recursive.
requires python3.10 (due to use of match statements)

To see it in action just run `core.py`.

## hello world example
```xml
<print>
    <lit> "Hello, World!" </lit>
</print>
```

## syntax notes
### literal and names
names are just empty tags like `<x />` or `<x></x>`.
literals are a little more complicated, they are text only tags. The text they contain is passed to python's `ast.literal_eval` so they have to follow the same rule as pythons literals, though with restrictions. there are some examples below;
```xml
<block>
    <!-- int !-->
    <lit> 69 </lit>
    <!-- float !-->
    <lit> 420.0 </lit>
    <!-- string !-->
    <lit> "spam, eggs, foo, bar, baz" </lit>
    <!-- complex !-->
    <lit> 3 + 1j </lit>
    <!-- bytes !-->
    <lit> b"\xca\xfe\xba\xbe" </lit>
</block>
```
other literals from python are also supported, though their use is not tested, at all.

### function calls
Function calls are done via adding child nodes to a node. This only supports directly calling functions. This makes the language feel more like a Lisp dialect, so `f(x)` is written closer to `(f x)` with `<f><x /></f>`.

## builtins and preludes
XML has a few builtin functions like `<print />`, `<block />`, `<list />`, `<map />`, and `<import />`. 
- `<print />` and `<list />` are just wrappers around the equivalent python functions. `<list />` is modified to act like `(*args) => [*args]` because it allows for `<list> <x /> <y /> <z /> </list>` which is nice.
- `<map />` is like the python builtin map, only it returns a list. 
- `<block />` takes any number of arguments, evaluates all of them and returns the result of the last one.
- `<import />` currently isn't fully implemented, it can only import python moduless currently. Imports currently look like `<import> <external /> <somePythonModule /> </import>`.

XML also has a few functions imported by default in its prelude library. This includes pythons `operator` library, aswell as `getattr`, `setattr`, and `range`.

## examples
examples can be found in the examples folder and can be ran via the `xmli.py` script.