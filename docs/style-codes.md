# Style Codes

This page describes in detail the format used to encode a style judgement into a style code.

## Requirements

The encoding was designed to produce a _representation_ (alphanumeric word) of a style judgement with the following requirements: 

* _Completeness_: the representation should contain all the information in the style judgement.
* _Human readability_: the representation should not entirely depend on computerized systems to be in-
terpreted; important data about it must be human
readable in case electronic processing means are not available.
* _Clarity and conciseness_: the representation is communicated verbally by the style judge to the field assistant; for this reason, it is important that the likelihood of errors in communication/data entering is minimal.

## Representation

Style codes follow this format:

    aXXbcYZ

where:

* `a` is a letter from the 26-letter English alphabet,
* `XX` is a 1- or 2-digit number,
* `b` (optional) is a letter from the English alphabet with _i_ and _o_ removed (a set of 24 letters),
* `c` (optional, requires `b`) is a letter from the 26-letter English alphabet,
* `Y` (optional, requires `b`) is a 1-digit number,
* `Z` (optional, requires `Y`) is a 1-digit number or a letter between _a_ and _l_ (excluding _i_).

The representation is case-insensitive.

The format and the encoding algorithm is chosen with the following considerations:

* Important information is human-readable. `XX` is the total number of points assigned in all categories, `Y` is the value of `SOG` and `Z` is the value of `PEN`. So a code of `f9py21` encodes 9 points, 2 `SOG` and 1 penalty, for a total score of

  5.5 + 9 * 0.2 + 2 * 0.1 - 1 * 0.5 = 7.0.

* The codes always start with a letter. This ensures that they are interpreted as text (and not e.g. numbers) when entered in spreadsheet software.
* The encoding produces short codes for the more common results; longer codes are only generated for less common combination of points. For example, the common result `BAS` = `MOV` = `DIN` = `GCC` = 1 is encoded as `n4`.
* Letters which may be misread as numbers (_i_ and _o_) are excluded from positions where they can cause ambiguity in the resulting codes.

## The Algorithm

A style judgement consists in 7 scores between 0 and 3, a `SOG` score (between 0 and 3), and a `PEN` score (between 0 and 20).

`SOG` and `PEN` are encoded in the fields `Y` and `Z` respectively. If `PEN` is 10 or larger, then letters are used, with `a`=1, `b`=2, ..., `h`=17, `i` is excluded, `j`=18, `k`=19 and `l`=20. `Z` is omitted if `PEN` is zero, and `Y` is omitted if both `SOG` and `PEN` are zero.

The other 7 scores are encoded in the first part of the code, with format `aXXbc`. The numeric field `XX` contains the total of assigned points in these categories, so only 6 scores need to be encoded in the fields `a`, `b` and `c`, the seventh being the difference between the total and the sum of the other six. The `BAS` score is chosen as the one to be encoded in this way.

The fields `b` and `c` are optional. When only the `a` field is used (_one-letter format_), 26 scores can be encoded. These are used for the 26 most common scores, which are those for which `COM`, `SAPD` and `DIF` are zero and `MOV`, `DIN` and `GCC` have values 0, 1, or 2. These conditions account for 3^3 = 27 combinations, so the combination `MOV` = `DIN` = `GCC`= 3 has also been excluded from the one-letter format.

 If `SOG` or `PEN` are different from zero (so `Y` cannot be omitted), and the one-letter format is being used, then `b` takes the value `z` to be used as a separator between `XX` and `Y` for maximum clarity.

When the fields `a` and `b` are used (_two-letters format_), 23 * 26 = 598 combinations can be represented. This format is used to represent all combinations for which `MOV`, `DIN` and `GCC` have any values (4^3 = 64) and `COM`, `SAPD`, and `DIF` have values 0 or 1 (2^3 = 8), for a total of 64 * 8 = 512 combinations, that fit in the 598 representable combinations.

Then all three fields are used (_three-letters format_) we can represent 26 * 26 * 23 = 15548 values, enough to represent all combinations of the six categories (4^6 = 4096).

As is apparent from the description above, there are 86 unused combinations in the two-letters format which could, in principle, be used to encode combinations that now require the three-letters format. However, this would cause the encoding algorithm to become more complicated for a relatively little gain. 

Here follows a C-like pseudocode detailing the exact encoding used to generate the `a`, `b` and `c` fields. Here, `encode26(i)` produces the i-th letter of the 26-letter English alphabet, while `encode23(i)` produces the i-th letter of the English alphabet without _i_, _o_ and _z_.

    if ((COM == 0 && SAPD == 0 && DIF == 0)
    && (MOV + DIN + GCC < 6)
    && (MOV < 3 && DIN < 3 && GCC < 3)) {
        // One-letter format
        a = encode26((MOV * 3 + DIN) * 3 + GCC);
    } else if (SAPD < 2 && COM < 2 && DIF < 2) {
        // Two-letters format
        value = (((((MOV * 4 + DIN) * 4 + GCC) * 4 + COM) * 2 + SAPD) * 2 + DIF);
        a = encode26(value / 23);
        b = encode23(value % 23);
    } else {
        // Three-letters format
        value = (((((MOV * 4 + DIN) * 4 + GCC) * 4 + COM) * 4 + SAPD) * 4 + DIF);
        a = encode26(value / (23 * 26));
        remainder = value % (23 * 26);
        b = encode23(remainder / 26);
        c = encode26(remainder % 26);
    }