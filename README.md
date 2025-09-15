# INCOM Style Codes

Documentation and utilities for INCOM Style Codes.

**Current version: 2 (Valid from 2025-09-14)**

* The `docs` folder contains the documentation, rendered at [https://anfive.github.io/style-codes/](https://anfive.github.io/style-codes/).
* The `python`, `typescript` and `php` folders contain implementations of encode and decode functions that can be used to encode and decode Style Codes.

# Example implementations

The code in the example implementations can be used freely ([Unlicense](https://unlicense.org/)).
If the files are run as scripts, they will run the following tests:
 * Generate all possible style judgement
 * Encode them and check that they all encode to unique style codes (no code collision)
 * Decode them and check that they all decode to the original style judgement

By default, the scripts dump all codes as JSON to text files. You can then use file comparison/hashing tools to verify that the implementations produce the same codes.

To run the files as scripts:

```bash
python python/style_codes_v2b.py
```

```bash
tsx typescript/style_codes_v2b.ts
```

```bash
php php/style_codes_v2b.php
```

It would be useful to test that all invalid codes are correctly detected (and not decoded to a style judgement). Feel free to do this if you want.

# Contibuting

If you find a bug or would like to improve the code, please open an issue or a pull request. Any contributions will need to be submitted under the Unlicense.