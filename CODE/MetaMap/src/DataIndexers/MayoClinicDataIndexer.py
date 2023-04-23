import requests
import os
import json
import time
from src.MetaMap import MetaMap

CURRENT_DIR = os.path.dirname(__file__)
MAYO_CLINIC_HOME_PAGE = 'https://www.mayoclinic.org'

start_index = 0
end_index = 1182

def remove_non_ascii(text):
    """Function to remove non-ASCII characters from a string"""
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def index_json_file(file_path):
    """Function to index a JSON file containing crawled web pages from Mayo Clinic website"""
    # Initialize MetaMapWrapper object
    mmw = MetaMap()

    # Open the JSON file containing crawled web pages data
    with open(file_path) as json_file:
        data = json.load(json_file)
        failed_count = 0
        for post_id in range(start_index, end_index):
            # Wait for 0.25 seconds before every request
            time.sleep(0.25)
            try:
                preprocessed_page = {}

                # Get the link and health condition for the current page
                page_data = data[str(post_id)]
                link = page_data['link'].replace('\\', '')
                temp = link[len('diseases-conditions')+2:]
                health_condition = temp[0: temp.find('/')]
                
                # Add the health condition and page URL to the preprocessed page dictionary
                preprocessed_page['health_condition'] = health_condition
                preprocessed_page['page_url'] = MAYO_CLINIC_HOME_PAGE + link
                
                if 'symptoms' in page_data:
                    symptoms_text = ''
                    symptoms = page_data['symptoms']
                    for symptom in symptoms:
                        symptoms_text += ' ' + symptom
                        
                    # Add the symptoms text to the preprocessed page dictionary
                    preprocessed_page['symptoms_text'] = symptoms_text
                    
                    # Remove non-ASCII characters from symptoms text as MetaMap causes tagging issue with them
                    symptoms_text = remove_non_ascii(symptoms_text)
                    
                    # Use MetaMap to extract symptoms, diseases, and diagnostic procedures from symptoms text
                    extracted_data = mmw.annotate(symptoms_text)
                    if 'symptoms' in extracted_data:
                        preprocessed_page['symptoms'] = extracted_data['symptoms']
                    if 'diseases' in extracted_data:
                        preprocessed_page['diseases'] = extracted_data['diseases']
                    if 'diagnostics' in extracted_data:
                        preprocessed_page['diagnostic_procedures'] = extracted_data['diagnostics']

                # Send a POST request to the server to index the preprocessed page data
                r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "mayo_clinic"},
                                  json=preprocessed_page)
                if r.status_code == 500:
                    failed_count += 1

            except Exception as e:
                # Handle any exception that occurs during the indexing of the current page
                print("Exception while indexing this page: " + str(page_data))
                print('Exception message: ' + str(e))
                failed_count += 1

    # Send a final index commit request to the server
    r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "index_commit"},
                      json={"status": "ok"})
    print("Commit status: " + str(r.status_code))

    # Print the total number of failed requests
    print("Total number of failed requests: " + str(failed_count))

