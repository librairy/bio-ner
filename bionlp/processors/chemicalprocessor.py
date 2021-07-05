from .bioprocessor import BioProcessor
import pysolr
from bionlp.processors.utils import unique_terms
import re
import os

class ChemicalProcessor(BioProcessor):

    def __init__(self, model_name):
        super().__init__(model_name)
        self.solr_url = os.getenv('SOLR_URL','http://localhost:8983/solr/')
        try:
            self.solr_engine = pysolr.Solr(self.solr_url+'bioner-drugs', timeout=20)
        except ConnectionError:
            print('Connection with Solr Chemical database could not be established')

    def normalize_chemical_entities(self, chemical_ents):
        normalized_chems = []
        chems = unique_terms(chemical_ents)
        for chem in chems:
            try:
                label = str(chem)
                solr_query_strict = "term:\"" + label + "\"^100 or synonyms:\"" + label + "\"^10 or mesh_headings:\"" + label + "\"^5"
                solr_query_lax = "term:" + label + "^100 or synonyms:" + label + "^10 or mesh_headings:" + label + "^5"
                solr_query_strict_syn = "term:\"" + label + "\"^10 or synonyms:\"" + label + "\"^100 or mesh_headings:\"" + label + "\"^5"
                solr_query_lax_syn = "term:" + label + "^10 or synonyms:" + label + "^100 or mesh_headings:" + label + "^5"
                results_lax = self.solr_engine.search(solr_query_lax, **{'fl': '*,score'})
                results_strict = self.solr_engine.search(solr_query_strict, **{'fl': '*,score'})
                results_lax_synonyms = self.solr_engine.search(solr_query_lax_syn, **{'fl': '*,score'})
                results_strict_synonyms = self.solr_engine.search(solr_query_strict_syn, **{'fl': '*,score'})
            except Exception:
                label = re.sub(r'\W+', ' ', str(chem))
                try:
                    solr_query_strict = "term:\"" + label + "\"^100 or synonyms:\"" + label + "\"^10 or mesh_headings:\"" + label + "\"^5"
                    solr_query_lax = "term:" + label + "^100 or synonyms:" + label + "^10 or mesh_headings:" + label + "^5"
                    solr_query_strict_syn = "term:\"" + label + "\"^10 or synonyms:\"" + label + "\"^100 or mesh_headings:\"" + label + "\"^5"
                    solr_query_lax_syn = "term:" + label + "^10 or synonyms:" + label + "^100 or mesh_headings:" + label + "^5"
                    results_lax = self.solr_engine.search(solr_query_lax, **{'fl': '*,score'})
                    results_strict = self.solr_engine.search(solr_query_strict, **{'fl': '*,score'})
                    results_lax_synonyms = self.solr_engine.search(solr_query_lax_syn, **{'fl': '*,score'})
                    results_strict_synonyms = self.solr_engine.search(solr_query_strict_syn, **{'fl': '*,score'})
                except Exception:
                    continue

            if len(results_lax) < 1 and len(results_strict) < 1:
                chemical = {'text_term': label}
                normalized_chems.append(chemical)
            else:
                # print(label)
                score_lax = 0
                score_strict = 0
                score_lax_syn = 0
                score_strict_syn = 0
                for result in results_lax:
                    # print(result['term'])
                    score_lax = result['score']
                    # print(score_lax)
                    break
                for result in results_strict:
                    # print(result['term'])
                    score_strict = result['score']
                    # print(score_strict)
                    break
                for result in results_strict_synonyms:
                    # print(result['term'])
                    score_strict_syn = result['score']
                    # print(score_strict_syn)
                    break
                for result in results_lax_synonyms:
                    # print(result['term'])
                    score_lax_syn = result['score']
                    # print(score_lax_syn)
                    break
                results_scores = {results_lax: score_lax, results_strict: score_strict,
                                  results_strict_synonyms: 0.8*score_strict_syn, results_lax_synonyms: 0.8*score_lax_syn}
                results = max(results_scores, key=results_scores.get)
                # print('----------')
                for result in results:
                    chemical = {}
                    chemical["text_term"] = label
                    if "term" in result:
                        chemical["found_term"] = "".join(result["term"])
                    if 'cid' in result:
                        chemical['cid'] = result["cid"]
                    if 'mesh_id' in result:
                        chemical['mesh_id'] = result["mesh_id"]
                    if 'chebi_id' in result:
                        chemical['chebi_id'] = result["chebi_id"]
                    if 'cross_references' in result:
                        chemical['cross_references'] = result["cross_references"]
                    if 'ATC' in result:
                        chemical['ATC'] = "".join(result["ATC"])
                    if 'ATC_level' in result:
                        chemical['ATC_level'] = result["ATC_level"]
                    normalized_chems.append(chemical)
                    break
        return normalized_chems
