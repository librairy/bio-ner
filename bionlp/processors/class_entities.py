from spacy import util

class Entities:

    def __init__(self, doc):
        self.doc = doc
        self.ents = []

    def __len__(self):
        return len(self.doc.ents)
    
    def sort_entities(self):
        self.ents = sorted(self.ents, key=lambda k: k['start'])

    def append_new_entities(self, entities):
        self.ents += entities

    def remove_non_entities(self):
        for ent in self.ents:
            if ent['entity_group'] == '0':
                self.ents.remove(ent)

    def postprocessing(self):
        def correct_boundaries():
            last_ent = {'entity_group': '0', 'score': 1, 'word': '', 'start': 0, 'end': 0}
            for ent in self.ents:
                if (ent['entity_group'] == last_ent['entity_group']) and (ent['start'] == last_ent['end']):
                    ent['start'] = last_ent['start']
                    if ent['word'].startswith('##'):
                        ent['word'] = ent['word'].replace('##', '')
                    ent['word'] = last_ent['word'] + ent['word']
                    self.ents.remove(last_ent)
                last_ent = ent

        def ents_spans_spacy_doc():
            ent_spans = []
            for ent in self.ents:
                proposed_ent = self.doc.char_span(ent['start'], ent['end'], ent['entity_group'])
                if proposed_ent:
                    ent_spans.append(proposed_ent)
            return ent_spans

        def solve_split_words(ent_spans):
            proposed_ents = []
            for i, ent in enumerate(self.ents):
                proposed_ent = self.doc.char_span(ent['start'], ent['end'], ent['entity_group'])
                if not proposed_ent:
                    proposed_ents.append(ent)
            for i, ent in enumerate(proposed_ents):
                if ent['word'].startswith('##') and (proposed_ents[i - 1]['entity_group'] == ent['entity_group']) and (
                        (ent['start'] - proposed_ents[i - 1]['end']) < 10) and (proposed_ents[i - 1]['start'] < ent['end']):
                    new_ent = self.doc.char_span(proposed_ents[i - 1]['start'], ent['end'], ent['entity_group'])
                    # print(new_ent)
                    ent_spans.append(new_ent)
            return ent_spans

        try:
            self.remove_non_entities()
            self.sort_entities()
            correct_boundaries()
            ent_spans = ents_spans_spacy_doc()
            ent_spans = solve_split_words(ent_spans)
            ent_spans = list(filter(None, ent_spans))
            filtered_spans = util.filter_spans(ent_spans)
            self.doc.set_ents(filtered_spans)
        except ValueError:
            print('An error happened')
        # print(self.doc.ents)

