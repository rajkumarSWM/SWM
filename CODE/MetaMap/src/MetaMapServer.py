from flask import Flask, request, jsonify
from MetaMap import MetaMap
from SimilarSymptoms import SimilarSymptoms
import networkx as nx
import pickle
import os

CURRENT_DIR = os.path.dirname(__file__)
GRAPH_PKL_PATH = os.path.join(CURRENT_DIR, 'graph.pkl')
SYMPTOMS_PKL_PATH = os.path.join(CURRENT_DIR, 'symptoms.pkl')

app = Flask(__name__)
mmw = MetaMapWrapper()

# PPR
G = nx.Graph()
symptoms = set()
with open(SYMPTOMS_PKL_PATH, 'rb') as f:
    symptoms = pickle.load(f)
    print(len(symptoms))
with open(GRAPH_PKL_PATH, 'rb') as f:
    G = pickle.load(f)
    print(G)
ss = SimilarSymptoms()

@app.route('/')
def index():
    return 'Server is running.'

@app.route('/search', methods=['GET'])
def search():
    search_query_str = request.args.get('query')
    extracted_data = mmw.annotate(search_query_str)
    annotated_query = {}

    if 'symptoms' in extracted_data:
        annotated_query['symptoms'] = extracted_data['symptoms']
    if 'diseases' in extracted_data:
        annotated_query['diseases'] = extracted_data['diseases']
    if 'diagnostics' in extracted_data:
        annotated_query['diagnostic_procedures'] = extracted_data['diagnostics']

    # PPR to fetch similar symtpoms
    # args - <Graph(loaded from pkl), symptoms(loaded from pkl), list of user symptoms, limit of returned symptoms(default-5)>
    # returns - list of similar symptoms
    if 'symptoms' in annotated_query:
        extracted_data['symptoms_suggestion'] = ss.get_similar_symptoms(G, symptoms, annotated_query['symptoms'])

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
