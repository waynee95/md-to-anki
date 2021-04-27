# md-to-anki

> Convert markdown to Anki cards

Just another tool to convert markdown to [Anki](https://apps.ankiweb.net/) cards.
Partially inspired by [mdanki](https://github.com/ashlinchak/mdanki).

:warning: This tool is mostly for my own usage. Use at your own risk.

## Usage

```
## Question

Front

%

Back
```

Each card is separated by `---`.

```
$ pip install -r requirements.txt
$ ./md-to-anki test/test.md test.apkg
```

## TODO

- [ ] Add option to specify directory
- [ ] Add option to specify deck name
- [ ] Add option to generate one or multiple decks

## License

[MIT](/LICENSE)
