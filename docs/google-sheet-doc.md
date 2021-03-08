# Google Sheet Template for Style Codes Processing

This Google Sheet file contains scripts that provide custom functions to work with (encode/decode) Style Codes:

https://docs.google.com/spreadsheets/d/1pdy_-UQw_h0NvIQdKBk77XaIAOvfHBOWbTrDGGOZf5g

## How to use the file

You will need a Google account to use the file (of course).
The file cannot be edited, you will have to create your own copy of the file and work in the copy.

__IMPORTANT__:
* You need to __make a copy__ of the file in order for the scripts to be copied with it. You cannot just copy-paste the contents of the file.
* When you create a copy, Google will create a new Apps Script project belonging to you. The project will contain a copy of the code. You can see your Apps Script project in the Google Apps Script dashboard: https://script.google.com/home

Follow this procedure:
* Open the file
* From the _File_ menu, select _Make a copy_.
* Edit the copied file.

The file contains some examples on how to use the functions. You can build on those or just delete everything and create your own document using those functions.

## Encoding Style Codes

Encoding is done using the `incom_style_encode()` function. The function signature is:

    =incom_style_encode(bas; mov; din; com; sapd; gcc; dif; sog; pen)

All arguments must be integers. All arguments except `pen` must have values between 0 and 3 (included). `pen` must have a value between 0 and 20 (included).

The function returns the Style Code corresponding to this judgement (a string), or an error if the values are incorrect.

For example,

    =incom_style_encode(1; 2; 1; 1; 0; 2; 1; 0; 1)

returns `n8l01`.

## Decoding Style Codes or Computing the Score

Decoding is done using the `incom_style_decode()` function. The function signature is:

    =incom_style_decode(code; value)

where `code` is a Style Code (a string) and `value` is the value that must be returned. The function returns a numeric value corresponding to the requested `value`, or an error if the arguments are invalid.

The requested `value` can be:

* `score`: the Style score (a value from 0.0 to 10.0).
* `points`: the sum of all points assigned in all categories, except `SOG` and `PEN`.
* one of `bas`, `mov`, `din`, `com`, `sapd`, `gcc`, `dif`, `sog`, `pen`: the corresponding value in the Style judgement.
* `all` for bulk decoding, see below.

For example:

* `=incom_style_decode("n8l01", "score")` returns `6.6`.
* `=incom_style_decode("n8l01", "points")` returns `8`.
* `=incom_style_decode("n8l01", "mov")` returns `2`.
* `=incom_style_decode("n8l01", "pen")` returns `1`.

## Bulk Decoding a Style Code

Custom functions in Google Sheet (such as the ones implemented in the script) take some time to execute. The following can speed up processing if a lot of data is involved, for example, all the style codes collected in a tournament.

The function `incom_style_decode()` can produce all values at once by specifying `all` as the requested value. The values will be written in the cells below the formula. For example,

    =incom_style_decode("n8l01", "all")

will fill its cell with the Score and the 9 cells beneath it with the individual values (`bas`, `mov`, etc.).

The helper function `incom_style_decode_titles()` is also provided to help with using this method. The function will fill its cell and the 9 beneath it with titles describing the values produced by `incom_style_decode(<code>, "all")`

Alternatively, for an even more efficient approach, consider using [the separate command-line program `servizio-cli`](https://github.com/anfive/servizio-cli) to bulk-decode an entire file.

## Further Work

Having a template document that users must copy is not optimal.
If you have experience on creating add-ons for Google Sheet and are available to work on one, please let me know.
