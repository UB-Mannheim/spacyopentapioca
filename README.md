# spaCyOpenTapioca

[![PyPI version](https://badge.fury.io/py/spacyopentapioca.svg)](https://badge.fury.io/py/spacyopentapioca) <a href="https://ub-mannheim.github.io/spacyopentapioca"><img src="https://img.shields.io/badge/docs-JB-green.svg"/></a> <a href="https://mybinder.org/v2/gh/UB-Mannheim/spacyopentapioca/main?urlpath=tree/docs/docs/demo.ipynb"><img src="https://img.shields.io/badge/launch-binder-blue.svg"/></a>

A [spaCy](https://spacy.io) wrapper of [OpenTapioca](https://opentapioca.org) for named entity linking on Wikidata.

## Table of contents
* [Installation](#installation)
* [How to use](#how-to-use)
* [Local OpenTapioca](#local-opentapioca)
* [Vizualization](#vizualization)

## Installation

```shell
pip install spacyopentapioca
```

or
```shell
git clone https://github.com/UB-Mannheim/spacyopentapioca
cd spacyopentapioca/
pip install .
```

## How to use

After installation the OpenTapioca pipeline can be used without any other pipelines:
```python
import spacy
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca', config={"verify": False})
doc = nlp("Christian Drosten works in Germany.")
for span in doc.ents:
    print((span.text, span.kb_id_, span.label_, span._.description, span._.score))
```
```shell
('Christian Drosten', 'Q1079331', 'PERSON', 'German virologist and university teacher', 3.6533377082098895)
('Germany', 'Q183', 'LOC', 'sovereign state in Central Europe', 2.1099332471902863)
```

Note the optional `verify` parameter of config defaults to `True`. If the URL is not secure this parameter must be `False` for the pipeline to work. For example, the default [URL](https://opentapioca.wordlift.io/) is not secure and requires this parameter to be `False`. See [https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings](https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings) for more details.

The types and aliases are also available:
```python
for span in doc.ents:
    print((span._.types, span._.aliases[0:5]))
```
```shell
({'Q43229': False, 'Q618123': False, 'Q5': True, 'P2427': False, 'P1566': False, 'P496': True}, ['كريستيان دروستين', 'Крістіан Дростен', 'Christian Heinrich Maria Drosten', 'کریستین دروستن', '크리스티안 드로스텐'])
({'Q43229': True, 'Q618123': True, 'Q5': False, 'P2427': False, 'P1566': True, 'P496': False}, ['IJalimani', 'R. F. A.', 'Alemania', '도이칠란트', 'Germaniya'])
```

The Wikidata QIDs are attached to tokens:
```python
for token in doc:
    print((token.text, token.ent_kb_id_))
```
```shell
('Christian', 'Q1079331')
('Drosten', 'Q1079331')
('works', '')
('in', '')
('Germany', 'Q183')
('.', '')
```

The raw response of the OpenTapioca API can be accessed in the doc- and span-objects:
```python
raw_annotations1 = doc._.annotations
raw_annotations2 = [span._.annotations for span in doc.ents]
```

The partial metadata for the response returned by the OpenTapioca API is
```python
doc._.metadata
```

All span-extensions are:
```python
span._.annotations
span._.description
span._.aliases
span._.rank
span._.score
span._.types
span._.label
span._.extra_aliases
span._.nb_sitelinks
span._.nb_statements
```

Note that spaCyOpenTapioca does a tiny processing of entities appearing in `doc.ents`. All entities returned by OpenTapioca can be found in `doc.spans['all_entities_opentapioca']`.
### Batching

Batched asynchronous requests to the OpenTapioca API via `nlp.pipe(List[str])`:
```python
import spacy
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca', config={"verify": False})
docs = nlp.pipe(
    [
        "Christian Drosten works in Germany.",
        "Momofuku Ando was born in Japan.".
    ]
)
for doc in docs:
    for span in doc.ents:
        print((span.text, span.kb_id_, span.label_, span._.description, span._.score))

```
```shell
('Christian Drosten', 'Q1079331', 'PERSON', 'German virologist and university teacher', 3.6533377082098895)
('Germany', 'Q183', 'LOC', 'sovereign state in Central Europe', 2.1099332471902863)
('Momofuku Ando', 'Q317858', 'PERSON', 'Taiwanese-Japanese businessman', 3.6012208212234302)
('Japan', 'Q17', 'LOC', 'sovereign state in East Asia, situated on an archipelago of five main and over 6,800 smaller islands', 2.349944834167907)
```

## Local OpenTapioca

If OpenTapioca is deployed locally, specify the URL of the new OpenTapioca API in the config:
```python
import spacy
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca', config={"url": OpenTapiocaAPI, "verify": False})
doc = nlp("Christian Drosten works in Germany.")
```
## Vizualization

NEL vizualization is added to spaCy via [pull request 9199](https://github.com/explosion/spaCy/pull/9199) for [issue 9129](https://github.com/explosion/spaCy/issues/9129). It is supported by spaCy >= 3.1.4.

Use manual option in displaCy:
```python
import spacy
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca', config={"verify": False})
doc = nlp("Christian Drosten works\n in Charité, Germany.")
params = {"text": doc.text,
          "ents": [{"start": ent.start_char,
                    "end": ent.end_char,
                    "label": ent.label_,
                    "kb_id": ent.kb_id_,
                    "kb_url": "https://www.wikidata.org/entity/" + ent.kb_id_}
                   for ent in doc.ents],
          "title": None}
spacy.displacy.serve(params, style="ent", manual=True)
```
The visualizer is serving on http://0.0.0.0:5000

![alt text](https://github.com/UB-Mannheim/spacyopentapioca/blob/main/images/nel_vizualization.png)

In Jupyter Notebook replace `spacy.displacy.serve` by `spacy.displacy.render`.
