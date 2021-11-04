import logging
import spacy
import requests
from spacy.language import Language
from spacy.tokens import Span, Doc

log = logging.getLogger(__name__)

@Language.factory('opentapioca',
                  default_config={"url": "https://opentapioca.org/api/annotate"})
class EntityLinker(object):
    """Sends raw data to the OpenTapioca API. Attaches entities to the document."""

    def __init__(self, nlp, name, url):
        """Passes url. Registers OpenTapioca extensions for Doc and Span."""
        self.url = url
        Doc.set_extension("annotations", default=None, force=True)
        Doc.set_extension("metadata", default=None, force=True)
        Span.set_extension("annotations", default=None, force=True)
        Span.set_extension("description", default=None, force=True)
        Span.set_extension("aliases", default=None, force=True)
        Span.set_extension("rank", default=None, force=True)
        Span.set_extension("score", default=None, force=True)
        Span.set_extension("types", default=None, force=True)
        Span.set_extension("label", default=None, force=True)
        Span.set_extension("extra_aliases", default=None, force=True)
        Span.set_extension("nb_sitelinks", default=None, force=True)
        Span.set_extension("nb_statements", default=None, force=True)

    def __call__(self, doc):
        """Requests the OpenTapioca API. Attaches entities to spans and doc."""

        # Post request to the OpenTapioca API
        r = requests.post(url=self.url,
                          data={'query': doc.text},
                          headers={'User-Agent': 'spaCyOpenTapioca'})
        r.raise_for_status()
        data = r.json()

        # Attaches raw data to doc
        doc._.annotations = data.get('annotations')
        doc._.metadata = {"status_code": r.status_code, "reason": r.reason,
                          "ok": r.ok, "encoding": r.encoding}

        # Attaches indexes, label and QID to spans
        # Processes annotations: if 'best_qid'==None, then no annotation
        ents = []
        for ent in data.get('annotations'):
            start, end = ent['start'], ent['end']
            if ent.get('best_qid'):
                ent_kb_id = ent['best_qid']
                try:  # to identify the type of entities
                    t = ent['tags'][0]['types']
                    types = {'PERSON': t['Q5'] + t['P496'],
                             'ORG': t['Q43229'] + t['P2427'],
                             'LOC': t['Q618123'] + t['P1566']}
                    m = max(types.values())
                    etype = ''.join([k for k, v in types.items() if v == m])
                except Exception as e:
                    log.error(e, extra=ent)
                    etype = ''
                span = doc.char_span(start, end, etype, ent_kb_id)
            else:
                etype = ''
                span = doc.char_span(start, end, etype)
            if not span:
                span = doc.char_span(start, end, etype, ent_kb_id,
                                     alignment_mode='expand')
                log.warning('The OpenTapioca-entity',
                      ent['tags'][0]['label'][0], (start,end),
                      'does not fit the span', span.text,
                      (span.start_char, span.end_char), 'in spaCy. EXPANDED!')
            span._.annotations = ent
            span._.description = ent['tags'][0]['desc']
            span._.aliases = ent['tags'][0]['aliases']
            span._.rank = ent['tags'][0]['rank']
            span._.score = ent['tags'][0]['score']
            span._.types = ent['tags'][0]['types']
            span._.label = ent['tags'][0]['label']
            span._.extra_aliases = ent['tags'][0]['extra_aliases']
            span._.nb_sitelinks = ent['tags'][0]['nb_sitelinks']
            span._.nb_statements = ent['tags'][0]['nb_statements']
            ents.append(span)

        # Attach processed entities to doc.ents
        try:
            # this works with non-overlapping spans
            doc.ents = list(doc.ents) + ents
        except Exception:
            # filter the overlapping spans, keep the (first) longest one
            doc.ents = spacy.util.filter_spans(ents)
        # Attach all entities found by OpenTapioca to spans
        doc.spans['all_entities_opentapioca'] = ents
        return doc
