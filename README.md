# Java Property Escape Decoder

Decodes the escape sequences found in Java `.properties` files: `\u####`, `\n`, `\t`, `\r`, `\f`, and `\\`.

```python
from java_property_escape_decoder import decode

decode("line1\\nline2")        # -> "line1\nline2"
decode("caf\\u00e9")           # -> "caf\u00e9"
decode("a\\\\b")               # -> "a\\b"
```

## Why

`java.util.Properties` has its own small escape grammar that is close to, but not the same as, C-style or Python string escapes. When you read a `.properties` file from Python you need to turn those sequences back into characters without pulling in a full properties parser. This library does exactly that one job and nothing else: it does not split key/value pairs, strip leading whitespace, or join continued lines. The caller handles those steps, because that is where real-world properties files disagree with each other and with the spec.

## Exports

- `decode(text: str) -> str` — decode all recognised escapes in *text*.
- `decode_property_value(text: str) -> str` — same as `decode`, named for clarity when the input is a single logical value.

## Edge case you will hit

A backslash that is not followed by one of the recognised escape characters is left as a literal backslash. This matches `java.util.Properties`, which silently preserves unknown escapes rather than raising. So `decode("a\\xb")` returns `"a\\xb"`, not `"a" + chr(0x0b)`.

Surrogate pairs such as `\ud83d\ude00` decode to the corresponding astral character (U+1F600). Each `\u####` is resolved independently and the resulting surrogate code units are then combined by Python's string model, so no special pairing logic is needed.
