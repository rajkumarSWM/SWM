import networkx as nx
import sys, getopt
import pickle
import os


CURRENT_DIR = os.path.dirname(__file__)
GRAPH_PKL_PATH = os.path.join(CURRENT_DIR, 'graph.pkl')
SYMPTOMS_PKL_PATH = os.path.join(CURRENT_DIR, 'symptoms.pkl')

class SimilarSymptoms(object):


	def __init__(self):
    with open(SYMPTOMS_PKL_PATH, 'rb') as f:
        self.symptoms = pickle.load(f)
    with open(GRAPH_PKL_PATH, 'rb') as f:
        self.G = pickle.load(f)

def get_similar_symptoms(self, personal_symptoms, similar_limit=5):

    result = []

    personal_symptoms = [i.lower() for i in personal_symptoms]
    personalized = dict()
    found = False
    for i in personal_symptoms:
        if i in self.symptoms:
            personalized[i] = 1
            found = True

    if not found: 
        return result

    if len(personalized) > 0:
        pr = nx.pagerank(self.G, personalization=personalized, alpha=0.85)
    else:
        pr = nx.pagerank(self.G, alpha=0.85)
    ranking = [(key, val) for key, val in pr.items() if key not in personal_symptoms and key != 'symptoms']
    ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
    counter = 0

    for u, v in ranking:
        counter += 1
        result.append(u)

        if counter >= similar_limit:
            break

    return result


if __name__ == "__main__":

    symptoms = []
    limit = 5
    try:
        args = getopt.getopt(sys.argv[1:], "hs:l:", ["symptoms=","limit="])
    except getopt.GetoptError:
      print('filename.py -s <comma-separated symptoms> -l <number of results required>')
      sys.exit(2)

    for arg in args[0]:
        if '-s' in arg:
            symptoms = str(arg[1]).split(",")
        if '-l' in arg:
            limit = int(arg[1])

    rankings = similar_symptoms(symptoms, limit)
    print("Results for entered symptoms -", ",".join(symptoms))
    [print(str(i+1) + '. ' + ranking) for i, ranking in enumerate(rankings)]
