import flask
from flask import request, jsonify, abort
from flask import render_template
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown

from bionlp import nlp, disease_service, chemical_service, genetic_service

from spacy import displacy

colors = {"DISEASE": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
          "CHEMICAL": "linear-gradient(90deg, #ffa17f, #3575ad)",
          "GENETIC": "linear-gradient(90deg, #c21500, #ffc500)"}

app = flask.Flask(__name__)
Markdown(app)
CORS(app, support_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')



##################################################################################################
######
######          Bio NLP
######
##################################################################################################


@app.route('/bio-ner/entities', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def post_search_entities():
    if not request.json or not 'text' in request.json:
        abort(400)
    sequence = request.json['text']
    doc = nlp(sequence)

    entities_html = displacy.render(doc, style="ent",
                                    options={"ents": ["DISEASE", "CHEMICAL", "GENETIC", "DATE","GPE", "COVID LINEAGE"],
                                             "colors": colors})

    chemicals = [f.text for f in doc.ents if f.label_ == 'CHEMICAL']
    diseases = [f.text for f in doc.ents if f.label_ == 'DISEASE']
    genetics = [f.text for f in doc.ents if f.label_ == 'GENETIC']

    normalized_chems = chemical_service.normalize_chemical_entities(chemicals)
    normalized_dis = disease_service.normalize_disease_entities(diseases)
    normalized_gen = genetic_service.normalize_genetic_entities(genetics)
    normalized_covid = genetic_service.normalize_covid_entities(genetics+chemicals)

    normalized_ents = {'diseases': normalized_dis, 'chemicals': normalized_chems, 'genetics': normalized_gen,
                       'covid': normalized_covid}

    return jsonify(html=entities_html, entities=normalized_ents)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
