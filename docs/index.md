# INCOM Style Codes

Style Codes are a compact method to encode a style judgement in an alphanumeric word that uniquely identifies it. They can be used to quickly record complete style judgements effectively and in a short time, even if done by hand (for example during a tournament), which allows compiling detailed statistics afterwards.

The Style Codes format and the utilities below have been developed by Andrea "AnFive" Ferrario.

## Working with Style Codes

### Servizio App

The [Servizio app](https://play.google.com/store/apps/details?id=it.gnah.nordic.servizio) for Android is the main tool to work with Style Codes. The app is designed to be used by a Style Judge to grade simultaneously the two athletes taking part in a duel. The app also provides a Decode function to convert a Style Code back into the original judgement.
See the [Documentation for the Servizio app](servizio-app.md) for more information.

![Screenshot of the Servizio app](images/app/servizio-0.png)

### Google Sheet Template

There is a template Google Sheet that contains scripted formulas to encode/decode Style Codes. This document can be used as a starting point to create a Google Sheet to process Style Codes, for example a tournament board.
See the [Documentation for the Google Sheet template document](google-sheet-doc.md) for more information.

### The `servizio-cli` Command Line Utility

This is a command line utility (program) written in Rust that can be used to automate processing (encoding/decoding) Style Codes, for example in scripts or using .csv files.
The program is open source and [available on GitHub](https://github.com/anfive/servizio-cli).

## Style Codes, Explained

See the [Style Codes Documentation](style-codes.md) page for a detailed explanation of the Style Codes format.
