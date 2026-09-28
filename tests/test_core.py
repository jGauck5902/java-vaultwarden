import unittest

from java_property_escape_decoder import decode, decode_property_value


class DecodeTests(unittest.TestCase):
    def test_plain_string_unchanged(self):
        self.assertEqual(decode("hello world"), "hello world")

    def test_newline_escape(self):
        self.assertEqual(decode("line1\\nline2"), "line1\nline2")

    def test_tab_escape(self):
        self.assertEqual(decode("col1\\tcol2"), "col1\tcol2")

    def test_carriage_return_escape(self):
        self.assertEqual(decode("a\\rb"), "a\rb")

    def test_form_feed_escape(self):
        self.assertEqual(decode("a\\fb"), "a\fb")

    def test_backslash_escape(self):
        self.assertEqual(decode("a\\\\b"), "a\\b")

    def test_unicode_escape_lowercase(self):
        self.assertEqual(decode("\\u00e9"), "\u00e9")

    def test_unicode_escape_uppercase(self):
        self.assertEqual(decode("\\u00E9"), "\u00e9")

    def test_unicode_escape_surrogate_pair(self):
        # U+1F600 GRINNING FACE, encoded as a UTF-16 surrogate pair.
        self.assertEqual(decode("\\ud83d\\ude00"), "\U0001f600")

    def test_multiple_escapes_in_one_string(self):
        self.assertEqual(decode("a\\nb\\tc\\\\d"), "a\nb\tc\\d")

    def test_unknown_escape_left_literal(self):
        # A backslash not forming a recognised escape is kept as-is, matching
        # java.util.Properties which silently preserves such sequences.
        self.assertEqual(decode("a\\xb"), "a\\xb")

    def test_trailing_backslash_left_literal(self):
        self.assertEqual(decode("abc\\"), "abc\\")

    def test_empty_string(self):
        self.assertEqual(decode(""), "")

    def test_type_error_on_non_str(self):
        with self.assertRaises(TypeError):
            decode(b"bytes")  # type: ignore[arg-type]


class DecodePropertyValueTests(unittest.TestCase):
    def test_alias_behaviour(self):
        # decode_property_value is a thin named alias for decode, documenting
        # that the input is expected to be a single logical value. Asserting
        # equality of output keeps the two honest if they ever diverge.
        raw = "path\\\\to\\nfile"
        self.assertEqual(decode_property_value(raw), decode(raw))


if __name__ == "__main__":
    unittest.main()
