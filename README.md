# UnWiki
A parser that removes all wiki markup from the given string. Clean string is contained in the `decoded` attribute of the UnWiki class, either use `print()` or call `decoded` to access

## Example
```py
from unwiki import UnWiki

clean_text = UnWiki("{{ hello }} this {{ that }}")
print(clean_text) 
# this 
```


