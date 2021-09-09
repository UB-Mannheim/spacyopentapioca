import unittest
import spacy


class TestOpenTapioca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nlp = spacy.blank("en")
        nlp.add_pipe('opentapioca')
        cls.doc = nlp("Christian Drosten works in Germany")

    def test_opentapioca_api(self):
        self.assertEqual(self.doc._.metadata['ok'], True,
                         '"status_code" is not less than 400.')
        self.assertEqual(self.doc._.metadata['status_code'], 200,
                         '"status_code" is not 200.')

    def test_linking_two_entities(self):
        self.assertEqual(len(self.doc.ents), 2,
                         'Exactly two named entities should be linked.')

    def test_linked_entities_labels(self):
        self.assertEqual(self.doc.ents[0].text, "Christian Drosten",
                         'The first entity is not Christian Drosten.')
        self.assertEqual(self.doc.ents[1].text, "Germany",
                         'The second entity is not Germany.')


if __name__ == '__main__':
    unittest.main()
