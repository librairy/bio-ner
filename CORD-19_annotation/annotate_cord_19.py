import pysolr
import time
from os import path
import sys
from utils import group_in_dict
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

os.chdir('..')

from bionlp import nlp, disease_service, chemical_service, genetic_service

solr = pysolr.Solr('http://librairy.linkeddata.es/solr/cord19-paragraphs', always_commit=True, timeout=50)
completed = False
window_size = 500
paragraphs_processed = []
normalize_flag = False
nlp.max_length = 8000000
# fieldupdates = {'biobert_disease_ents': 'add',
#                 'biobert_chemical_ents': 'add',
#                 'biobert_genetic_ents': 'add',
#                 'biobert_chemical_normalized_term': 'add',
#                 'biobert_chemical_meshid': 'add',
#                 'biobert_chemical_cid': 'add',
#                 'biobert_chemical_chebi_id': 'add',
#                 'biobert_chemical_cross_references': 'add',
#                 'biobert_chemical_ATC': 'add',
#                 'biobert_chemical_ATC_level': 'add',
#                 'biobert_disease_normalized_term': 'add',
#                 'biobert_disease_meshid': 'add',
#                 'biobert_disease_cui': 'add',
#                 'biobert_disease_icd10': 'add',
#                 'biobert_disease_cross_references': 'add',
#                 'biobert_genetic_normalized_term': 'add',
#                 'biobert_genetic_ncbi_gene_id': 'add',
#                 'biobert_genetic_GO_id': 'add',
#                 'biobert_genetic_ncbi_taxon_id': 'add',
#                 'biobert_genetic_cross_references': 'add',
#                 'biobert_genetic_uniprot_id': 'add',
#                 'biobert_covid_normalized_term': 'add',
#                 'biobert_covid_evidence_url': 'add',
#                 'biobert_covid_target_url': 'add',
#                 'biobert_covid_association_score': 'add',
#                 'biobert_covid_ebi_reference': 'add',
#                 'biobert_covid_PR_id': 'add'
#                 }

if path.isfile('CORD-19_annotation/counter.txt'):
    with open('CORD-19_annotation/counter.txt', 'r') as f:
        counter = int(f.read())
    print('Resuming from ' + str(counter))
else:
    print('Starting annotation from beginning')
    counter = 0

if len(sys.argv) > 1:
    if sys.argv[1] == 'normalize':
        normalize_flag = True
        print('Normalization step activated')

if __name__ == '__main__':
    print("Start reading from solr...")
    while not completed:
        old_counter = counter
        try:
            paragraphs = solr.search(q="*:*", rows=window_size, start=counter, sort="id asc")

            for p in paragraphs:
                paragraph = {}
                paragraph['id'] = p['id']
                if ('section_s' in p):
                    paragraph['section_s'] = p['section_s']
                if ('article_id_s' in p):
                    paragraph['article_id_s'] = p['article_id_s']
                if ('size_i' in p):
                    paragraph['size_i'] = p['size_i']
                if ('name_s' in p):
                    paragraph['name_s'] = p['name_s']
                if ('text_t' in p):
                    paragraph['text_t'] = p['text_t']
                    try:
                        doc = nlp(str(paragraph['text_t']))
                        paragraph['biobert_disease_ents'] = list({f.text for f in doc.ents if f.label_ == 'DISEASE'})
                        paragraph['biobert_chemical_ents'] = list({f.text for f in doc.ents if f.label_ == 'CHEMICAL'})
                        paragraph['biobert_genetic_ents'] = list({f.text for f in doc.ents if f.label_ == 'GENETIC'})
                        if normalize_flag:
                            normalized_chem = chemical_service.normalize_chemical_entities(
                                paragraph['biobert_chemical_ents'])
                            normalized_d = disease_service.normalize_disease_entities(paragraph['biobert_disease_ents'])
                            normalized_g = genetic_service.normalize_genetic_entities(paragraph['biobert_genetic_ents'])
                            normalized_cov = genetic_service.normalize_covid_entities(paragraph['biobert_genetic_ents'])

                            normalized_chems = group_in_dict(normalized_chem)
                            normalized_dis = group_in_dict(normalized_d)
                            normalized_gen = group_in_dict(normalized_g)
                            normalized_covid = group_in_dict(normalized_cov)

                            if 'found_term' in normalized_chems:
                                paragraph['biobert_chemical_normalized_term'] = normalized_chems['found_term']
                            if 'mesh_id' in normalized_chems:
                                paragraph['biobert_chemical_meshid'] = normalized_chems['mesh_id']
                            if 'cid' in normalized_chems:
                                paragraph['biobert_chemical_cid'] = normalized_chems['cid']
                            if 'chebi_id' in normalized_chems:
                                paragraph['biobert_chemical_chebi_id'] = normalized_chems['chebi_id']
                            if 'cross_references' in normalized_chems:
                                paragraph['biobert_chemical_cross_references'] = normalized_chems['cross_references']
                            if 'ATC' in normalized_chems:
                                paragraph['biobert_chemical_ATC'] = normalized_chems['ATC']
                            if 'ATC_level' in normalized_chems:
                                paragraph['biobert_chemical_ATC_level'] = normalized_chems['ATC_level']

                            if 'found_term' in normalized_dis:
                                paragraph['biobert_disease_normalized_term'] = normalized_dis['found_term']
                            if 'mesh_id' in normalized_dis:
                                paragraph['biobert_disease_meshid'] = normalized_dis['mesh_id']
                            if 'cui' in normalized_dis:
                                paragraph['biobert_disease_cui'] = normalized_dis['cui']
                            if 'ICD10_id' in normalized_dis:
                                paragraph['biobert_disease_icd10'] = normalized_dis['ICD10_id']
                            if 'cross_references' in normalized_dis:
                                paragraph['biobert_disease_cross_references'] = normalized_dis['cross_references']

                            if 'found_term' in normalized_gen:
                                paragraph['biobert_genetic_normalized_term'] = normalized_gen['found_term']
                            if 'ncbi_gene_id' in normalized_gen:
                                paragraph['biobert_genetic_ncbi_gene_id'] = normalized_gen['ncbi_gene_id']
                            if 'GO_id' in normalized_gen:
                                paragraph['biobert_genetic_GO_id'] = normalized_gen['GO_id']
                            if 'ncbi_taxon_id' in normalized_gen:
                                paragraph['biobert_genetic_ncbi_taxon_id'] = normalized_gen['ncbi_taxon_id']
                            if 'cross_reference' in normalized_gen:
                                paragraph['biobert_genetic_cross_references'] = normalized_gen['cross_reference']
                            if 'uniprot_id' in normalized_gen:
                                paragraph['biobert_genetic_uniprot_id'] = normalized_gen['uniprot_id']

                            if 'found_term' in normalized_covid:
                                paragraph['biobert_covid_normalized_term'] = normalized_covid['found_term']
                            if 'evidence_url' in normalized_covid:
                                paragraph['biobert_covid_evidence_url'] = normalized_covid["evidence_url"]
                            if 'target_url' in normalized_covid:
                                paragraph['biobert_covid_target_url'] = normalized_covid["target_url"]
                            if 'association_score' in normalized_covid:
                                paragraph['biobert_covid_association_score'] = normalized_covid["association_score"]
                            if 'ebi_reference' in normalized_covid:
                                paragraph['biobert_covid_ebi_reference'] = normalized_covid["ebi_reference"]
                            if 'PR_id' in normalized_covid:
                                paragraph['biobert_covid_PR_id'] = normalized_covid["PR_id"]
                    except Exception as e:
                        print(repr(e))
                        paragraphs_processed.append(paragraph)
                        continue

                paragraphs_processed.append(paragraph)

            counter += len(paragraphs)

            if counter % window_size == 0:
                # print(paragraphs_processed[0])
                # solr.add(paragraphs_processed, fieldUpdates=fieldupdates)
                try:
                    solr.add(paragraphs_processed)
                except Exception as e:
                    print(repr(e))
                    print('Docs could not be indexed in position:',counter)
                print(counter, 'paragraphs annotated')
                paragraphs_processed = []
                with open('CORD-19_annotation/counter.txt', 'w') as f:
                    f.write(str(counter))

            if (old_counter == counter):
                print("done!")
                break

        except Exception as e:
            print(repr(e))
            print("Solr query error. Wait for 5secs..")
            time.sleep(5.0)
