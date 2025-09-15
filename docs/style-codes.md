# Style Codes (Version 2)

This page describes in detail the format used to encode a style judgement into a style code. It refers to the Version 2 of the Style Codes (supporting half points in the Technical Coefficients), in use since September 2025. For a description of the old version (supporting only integer points), see [Style Codes (Version 1)](style-codes-v1.md).

## Requirements

The encoding was designed to produce a _representation_ (alphanumeric word) of a style judgement with the following requirements: 

* _Completeness_: the representation should contain all the information in the style judgement.
* _Human readability_: the representation should not entirely depend on computerized systems to be in-
terpreted; important data about it must be human
readable in case electronic processing means are not available.
* _Clarity and conciseness_: the representation is communicated verbally by the style judge to the field assistant; for this reason, it is important that the likelihood of errors in communication/data entering is minimal.

## Representation

Style codes follow this format:

    abXXcdeYZ

where:

* `a`, `b`, `c`, `d`, `e` are letters from the English alphabet without _i_, _l_ and _o_, which can be ambiguous (a set of 23 letters).  `b`, `c`, `d`, `e` are optional and might not appear.
* `XX` is a 1- or 2-digit number,
* `Y` (optional, requires `c`) is a 1-digit number,
* `Z` (optional, requires `Y`) is a 1-digit number or a letter between _a_ and _m_ (excluding _i_ and _l_).

The representation is case-insensitive.

The format and the encoding algorithm is chosen with the following considerations:

* Important information is human-readable. `XX` is the total number of **half points** assigned in all categories, `Y` is the value of `SOG` and `Z` is the value of `PEN`. So a code of `eh5q12` encodes 5 half points, 2 `SOG` and 1 penalty, for a total score of

  5.5 + 5 * 0.1 + 2 * 0.1 - 1 * 0.5 = 5.7.

* The codes always start with a letter. This ensures that they are interpreted as text (and not e.g. numbers) when entered in spreadsheet software.
* The encoding produces short codes for the more common results; longer codes are only generated for less common combination of points. For example, the common result `BAS` = `MOV` = `GCC` = 1 is encoded as `r6`.
* Letters which may be misread as numbers (_i_, _l_ and _o_) are excluded.

## The Algorithm

A style judgement consists in 7 scores between 0 and 3 (with 0.5 interval), a `SOG` score (between 0 and 3), and a `PEN` score (between 0 and 20).

`SOG` and `PEN` are encoded in the fields `Y` and `Z` respectively. If `PEN` is 10 or larger, then letters are used, with `a`=1, `b`=2, ..., `h`=17, `i` is excluded, `j`=18, `k`=19, `l` is excluded, `m`=20. `Z` is omitted if `PEN` is zero, and `Y` is omitted if both `SOG` and `PEN` are zero.

The other 7 scores are encoded in the first part of the code, with format `abXXcde`. The numeric field `XX` contains the total of assigned half points in these categories, so only 6 scores need to be encoded in the letter fields, the seventh being the difference between the total and the sum of the other six. The `BAS` score is chosen as the one to be encoded in this way.

The fields from `b` to `e` are optional.

If `SOG` or `PEN` are different from zero (so `Y` cannot be omitted), and the one-letter format is being used, then `c` takes the value `z` to be used as a separator between `XX` and `Y` to prevent ambiguity.

The letter fields from `a` to `e` are computed by encoding a certain numeric value in base 23, using the following 23 letters as the digits: `zyxwvutsrqpnmkjhgfedcba` (`z` = 0, `y` = 1, `x` = 2, ...), so that the field `a` is the least significant digit and `e` is the most significant digit, and omitting most significant digits if the value is 0 (`z`).

The numeric value is computed from the values of the technical coefficients excluding `BAS`, so that the value is unique for all combinations of the technical coefficients. The formula for that value produces a smaller value for more common judgements (low values of `MOV`, `GCC` and `DIN`, and zero `COM`, `SAPD` and `DIF`). In the following, `//` is integer division and `%` is the remainder of integer division.

    mov_low_digit = (COM * 2) % 3
    mov_high_digit = (COM * 2) // 3
    din_low_digit = (DIN * 2) % 3
    din_high_digit = (DIN * 2) // 3
    gcc_low_digit = (GCC * 2) % 3
    gcc_high_digit = (GCC * 2) // 3

    value = mov_low_digit + \
        din_low_digit * 3 + \
        gcc_low_digit * 3 * 3 + \
        mov_high_digit * 3 * 3 * 3 + \
        din_high_digit * 3 * 3 * 3 * 3 + \
        gcc_high_digit * 3 * 3 * 3 * 3 * 3 + \
        com_int * 3 * 3 * 3 * 3 * 3 * 3 + \
        sapd_int * 3 * 3 * 3 * 3 * 3 * 3 * 7 + \
        dif_int * 3 * 3 * 3 * 3 * 3 * 3 * 7 * 7

Reference implementations
