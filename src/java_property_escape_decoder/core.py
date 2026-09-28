import re

_HEX_DIGIT = r"[0-9a-fA-F]"
# Match a backslash followed by one of the recognised escape characters, or a
# backslash followed by exactly four hex digits for a \\u#### sequence. Using a
# single regex keeps the scan to one pass; the alternation order matters because
# the \\u branch is more specific than the bare-backslash branch and must be
# tried first.
_ESCAPE = re.compile(
    r"\\(u(" + _HEX_DIGIT + r"{4})|n|t|r|f|\\)"
)


def _replace(match: re.Match) -> str:
    group = match.group(1)
    if group == "n":
        return "\n"
    if group == "t":
        return "\t"
    if group == "r":
        return "\r"
    if group == "f":
        return "\f"
    if group == "\\":
        return "\\"
    # \u#### branch
    return chr(int(match.group(2), 16))


def decode(text: str) -> str:
    """Decode Java properties file escape sequences in *text*.

    Recognised escapes are ``\\u####`` (four hex digits), ``\\n``, ``\\t``,
    ``\\r``, ``\\f``, and ``\\\\``. Any backslash not immediately followed
    by one of these is left as a literal backslash character, which mirrors how
    ``java.util.Properties`` treats unknown escapes rather than raising.
    """
    if not isinstance(text, str):
        raise TypeError("decode() requires a str")
    result = _ESCAPE.sub(_replace, text)
    # Re-encode as UTF-16-LE and decode so that surrogate pairs produced by
    # individual \u#### escapes combine into their astral characters, matching
    # java.util.Properties behaviour.
    return result.encode("utf-16-le", "surrogatepass").decode("utf-16-le")


def decode_property_value(text: str) -> str:
    """Decode a single logical property *value*.

    A logical value is what remains after line-continuation backslashes and
    leading whitespace have already been stripped by the caller. This function
    therefore only decodes the in-value escapes; it does not join continued
    lines. Keeping that step out of scope avoids guessing how the caller reads
    the file, which is where most properties parsers disagree.
    """
    return decode(text)
