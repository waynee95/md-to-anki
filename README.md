# md-to-anki

> Convert markdown to Anki cards

Just another tool to convert markdown to [Anki](https://apps.ankiweb.net/) cards.
Partially inspired by [mdanki](https://github.com/ashlinchak/mdanki).

:warning: This tool is mostly for my own usage. Use at your own risk.

## How to use

```
## Question

Front

%

Back
```

Each card is separated by `---`.

## Build a deck

```
$ pip install -r requirements.txt
$ ./md-to-anki --help
$ ./md-to-anki test/test.md test.apkg --deckname Test
```

## License

[MIT](/LICENSE)
