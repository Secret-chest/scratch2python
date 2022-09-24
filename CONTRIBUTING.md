## British English for docs, comments and names
Also correct the old ones written in American English. I recently switched (excuse me), and there's no going back.
This includes ending words in -ise and -yse, not -ize and -yze.
I have set my LanguageTool (I use PyCharm) to catch American English spellings, if you have it too, it may help.
The only exception is “colour”, American English is the
standard in programming so please use “color” in names. You should still use “colour” when not referring to a name.

If you don't know the differences, [this article on Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_American_and_British_English) may help you.

## Code style guidelines
For the most part, we follow PEP 8.

### Naming style
Use `mixedCase` for most names. For class names, use `CamelCase`.

### Quotes in code
Always use DOUBLE QUOTES (like `"this"`)! In some fonts single quotes look invisible.

### Indentation
Only use 4 spaces. I did not make commit checks yet (I will), but you should be sorry if you use anything other than 4
spaces in Python.

#### Hanging indents
For most hanging indents the rule is to align them with the opening, like these:
```python
someList = [1, 2, 3,
            4, 5, 6,]

if (1 == 1
    and 1 + 1 == 2
    and not "this".startswith("that")):
    # At least I have no problem with the confusion described in PEP 8.
    pass
```

### Comments
**Always** put a space after the pound sign (#)! Separate inline comments with two spaces from the rest of the line.

### Break before operators!
> To solve this readability problem, mathematicians and their publishers follow the opposite convention. Donald Knuth explains the traditional rule in his Computers and Typesetting series: “Although formulas within a paragraph always break after binary operations and relations, displayed formulas always break before binary operations”.
> Following the tradition from mathematics usually results in more readable code
> **- PEP 8**
```python
# Do it like described in PEP 8.

sum_ = (10000
      + 20000
      + 30000)
```

### Avoid backslashes. Use parentheses to be able to break lines when possible.

### Blank lines
> Surround top-level function and class definitions with two blank lines.
> Method definitions inside a class are surrounded by a single blank line.
> **- PEP 8**

Also group related code together and add some blank lines to separate it. Look at the source code already defined
to see examples of this. Do not add blank line _after_ comments! Don't worry, I will not reject your PR if you don't separate the code like I do.

### Imports on separate lines
```python
# This is right:
import os
import sys

# This is wrong:
import sys, os

# This is OK though:
from subprocess import Popen, PIPE
```

### Wildcard imports
Wildcard imports look like this:
```python
from json import *
```
Do not use them as they create confusion

### Whitespace should make sense
Whitespace in Python literally follows the rules of whitespace in English for punctuation.
For operators, the slice colon should have no space on either side, but all others should have one space
on either side. The equal in arguments (`function(x=y)`) should have no space though.

Avoid trailing whitespace as it's invisible and confusing.

