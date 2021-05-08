#!/usr/bin/env python3

import argparse
import genanki
import glob
import mistune
import os
import re
import sys

from HighlightRenderer import HighlightRenderer
markdown = mistune.create_markdown(renderer=HighlightRenderer())

cardSeparator = "---"
frontBackSeparator = "%"

parser = argparse.ArgumentParser()
parser.add_argument("input", help="either *.md file or a folder containing *.md files.")
parser.add_argument("output", help="name of the *.apkg file that will be generated.")
parser.add_argument("--deckname", default=None, help="name of the generated deck. If not specified, the name of the input will be used as the deckname.")
args = parser.parse_args()

input = args.input
output = args.output
deckname = args.deckname if args.deckname else input

model = genanki.Model(
  1234321,
  "My Model",
  fields = [{"name": "Question"}, {"name": "Answer"}],
  templates = [
    {
      "name": "Card 1",
      "qfmt": "{{Question}}",
      "afmt": "{{FrontSide}}<hr id=\"answer\">{{Answer}}",
    }
  ],
  css=".card { font-family: Arial, \"Helvetica Neue\", Helvetica, sans-serif; font-size: 16px; color: black; background-color: white; } .highlight { font-size: 0.9em; font-family: Monaco, Consolas, \"Courier New\", monospace; } .highlight .hll { background-color: #ffffcc } .highlight { background: #ffffff; } .highlight .c { color: #999988; font-style: italic } /* Comment */ .highlight .err { color: #a61717; background-color: #e3d2d2 } /* Error */ .highlight .k { color: #000000; font-weight: bold } /* Keyword */ .highlight .o { color: #000000; font-weight: bold } /* Operator */ .highlight .ch { color: #999988; font-style: italic } /* Comment.Hashbang */ .highlight .cm { color: #999988; font-style: italic } /* Comment.Multiline */ .highlight .cp { color: #999999; font-weight: bold; font-style: italic } /* Comment.Preproc */ .highlight .cpf { color: #999988; font-style: italic } /* Comment.PreprocFile */ .highlight .c1 { color: #999988; font-style: italic } /* Comment.Single */ .highlight .cs { color: #999999; font-weight: bold; font-style: italic } /* Comment.Special */ .highlight .gd { color: #000000; background-color: #ffdddd } /* Generic.Deleted */ .highlight .ge { color: #000000; font-style: italic } /* Generic.Emph */ .highlight .gr { color: #aa0000 } /* Generic.Error */ .highlight .gh { color: #999999 } /* Generic.Heading */ .highlight .gi { color: #000000; background-color: #ddffdd } /* Generic.Inserted */ .highlight .go { color: #888888 } /* Generic.Output */ .highlight .gp { color: #555555 } /* Generic.Prompt */ .highlight .gs { font-weight: bold } /* Generic.Strong */ .highlight .gu { color: #aaaaaa } /* Generic.Subheading */ .highlight .gt { color: #aa0000 } /* Generic.Traceback */ .highlight .kc { color: #000000; font-weight: bold } /* Keyword.Constant */ .highlight .kd { color: #000000; font-weight: bold } /* Keyword.Declaration */ .highlight .kn { color: #000000; font-weight: bold } /* Keyword.Namespace */ .highlight .kp { color: #000000; font-weight: bold } /* Keyword.Pseudo */ .highlight .kr { color: #000000; font-weight: bold } /* Keyword.Reserved */ .highlight .kt { color: #445588; font-weight: bold } /* Keyword.Type */ .highlight .m { color: #009999 } /* Literal.Number */ .highlight .s { color: #dd1144 } /* Literal.String */ .highlight .na { color: #008080 } /* Name.Attribute */ .highlight .nb { color: #0086B3 } /* Name.Builtin */ .highlight .nc { color: #445588; font-weight: bold } /* Name.Class */ .highlight .no { color: #008080 } /* Name.Constant */ .highlight .nd { color: #3c5d5d; font-weight: bold } /* Name.Decorator */ .highlight .ni { color: #800080 } /* Name.Entity */ .highlight .ne { color: #990000; font-weight: bold } /* Name.Exception */ .highlight .nf { color: #990000; font-weight: bold } /* Name.Function */ .highlight .nl { color: #990000; font-weight: bold } /* Name.Label */ .highlight .nn { color: #555555 } /* Name.Namespace */ .highlight .nt { color: #000080 } /* Name.Tag */ .highlight .nv { color: #008080 } /* Name.Variable */ .highlight .ow { color: #000000; font-weight: bold } /* Operator.Word */ .highlight .w { color: #bbbbbb } /* Text.Whitespace */ .highlight .mb { color: #009999 } /* Literal.Number.Bin */ .highlight .mf { color: #009999 } /* Literal.Number.Float */ .highlight .mh { color: #009999 } /* Literal.Number.Hex */ .highlight .mi { color: #009999 } /* Literal.Number.Integer */ .highlight .mo { color: #009999 } /* Literal.Number.Oct */ .highlight .sb { color: #dd1144 } /* Literal.String.Backtick */ .highlight .sc { color: #dd1144 } /* Literal.String.Char */ .highlight .sd { color: #dd1144 } /* Literal.String.Doc */ .highlight .s2 { color: #dd1144 } /* Literal.String.Double */ .highlight .se { color: #dd1144 } /* Literal.String.Escape */ .highlight .sh { color: #dd1144 } /* Literal.String.Heredoc */ .highlight .si { color: #dd1144 } /* Literal.String.Interpol */ .highlight .sx { color: #dd1144 } /* Literal.String.Other */ .highlight .sr { color: #009926 } /* Literal.String.Regex */ .highlight .s1 { color: #dd1144 } /* Literal.String.Single */ .highlight .ss { color: #990073 } /* Literal.String.Symbol */ .highlight .bp { color: #999999 } /* Name.Builtin.Pseudo */ .highlight .vc { color: #008080 } /* Name.Variable.Class */ .highlight .vg { color: #008080 } /* Name.Variable.Global */ .highlight .vi { color: #008080 } /* Name.Variable.Instance */ .highlight .il { color: #009999 } /* Literal.Number.Integer.Long */)"
)

deck = genanki.Deck(123454321, deckname)
media_files = []

def processMarkdownFile(file):
  fileContent = open(file).read()
  cardStrings = re.split(cardSeparator, fileContent)
  for cardString in cardStrings:
    front, back = cardString.split(frontBackSeparator)

    question = mistune.html(markdown(front.strip()))
    answer = mistune.html(markdown(back.strip()))
    note = genanki.Note(model=model, fields=[question,answer])
    deck.add_note(note)

def processMediaFile(file):
  media_files.append(file)

# TODO: Clean this mess up
if os.path.isdir(input):
  for file in os.listdir(input):
    if file.endswith((".md", ".markdown")):
      processMarkdownFile(os.path.join(input, file))
    elif file.lower().endswith((".png", ".jpg", ".jpeg", ".mp3")):
      processMediaFile(os.path.join(input,file))
else:
  if file.endswith((".md", ".markdown")):
    processMarkdownFile(os.path.join(input, file))
  elif file.lower().endswith((".png", ".jpg", ".jpeg", ".mp3")):
    processMediaFile(os.path.join(input,file))

package = genanki.Package(deck)
package.media_files = media_files
package.write_to_file(output)
