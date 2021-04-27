#!/usr/bin/env python3

import genanki
import mistune
import re
import sys

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'

markdown = mistune.create_markdown(renderer=HighlightRenderer())

model = genanki.Model(
  1234321,
  "Test Model",
  fields = [{"name": "Question"}, {"name": "Answer"}],
  templates = [
    {
      "name": "Card 1",
      "qfmt": "{{Question}}",
      "afmt": "{{FrontSide}}<hr id=\"answer\">{{Answer}}",
    }
  ],
  css=open("style.css").read()
)

deck = genanki.Deck(123454321, "Test Deck")

cardSeparator = "---"
frontBackSeparator = "%"

filePath = sys.argv[1]

with open(filePath) as f:
  cardStrings = re.split(cardSeparator, f.read())

  for cardString in cardStrings:
    front, back = cardString.split(frontBackSeparator)

    question = mistune.html(markdown(front.strip()))
    answer = mistune.html(markdown(back.strip()))
    note = genanki.Note(model=model, fields=[question,answer])
    deck.add_note(note)

package = genanki.Package(deck)
package.write_to_file(sys.argv[2])
