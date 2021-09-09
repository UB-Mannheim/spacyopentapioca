# spaCyOpenTapioca

A [spaCy](https://spacy.io) wrapper of [OpenTapioca](https://opentapioca.org) for named entity linking on Wikidata.

## Table of contents
* [Installation](#installation)
* [How to use](#how-to-use)
* [Local OpenTapioca](#local-opentapioca)

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
nlp.add_pipe('opentapioca')
doc = nlp("Christian Drosten works in Germany.")
for span in doc.ents:
    print((span.text, span.kb_id_, span.label_, span._.description, span._.score))
```
```shell
('Christian Drosten', 'Q1079331', 'PERSON', 'German virologist and university teacher', 3.6533377082098895)
('Germany', 'Q183', 'LOC', 'sovereign state in Central Europe', 2.1099332471902863)
```

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
```

Note that spaCyOpenTapioca does a tiny processing of entities appearing in `doc.ents`. All entities returned by OpenTapioca can be found in `doc.spans['all_entities_opentapioca']`.

## Local OpenTapioca

If OpenTapioca is deployed locally, specify the URL of the new OpenTapioca API in the config:
```python
import spacy
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca', config={"url": OpenTapiocaAPI})
doc = nlp("Christian Drosten works in Germany.")
```
