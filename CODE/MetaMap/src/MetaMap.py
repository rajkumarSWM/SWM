from pymetamap import MetaMap


class MetaMap(object):
    mm = MetaMap.get_instance('/Users/rajkumar/swm/MetaMap/public_mm/bin/metamap18')

    def __init__(self):
    pass

# This function will extract concepts from the given text and return the extracted data
def annotate(self, text):
    # Define the input for the MetaMap as list containing text
    mm_request = [text]

    # Extract concepts using MetaMap
    concepts, error = self.mm.extract_concepts(mm_request, [1, 2])

    # Define the empty dictionary to store extracted data
    extracted_data = {}
    symptoms = []
    diseases = []
    diagnostics = []

    # Loop through the extracted concepts
    for concept in concepts:
        # Check if the concept has the attribute 'semtypes'
        if hasattr(concept, 'semtypes'):
            # Check the type of the concept using 'semtypes' attribute
            if concept.semtypes == '[sosy]':
                # Sign or Symptom
                # Check if it's not 'Symptoms' as it is returned as a symptom sometimes
                if concept.preferred_name != 'Symptoms' and concept.preferred_name != 'symptoms':
                    symptoms.append(concept.preferred_name)
            elif concept.semtypes == '[dsyn]':
                # Disease or Syndrome
                diseases.append(concept.preferred_name)
                pass
            elif concept.semtypes == '[diap]':
                # Diagnostic Procedure
                diagnostics.append(concept.preferred_name)

    # Add the extracted data to the dictionary if they exist
    if len(symptoms):
        extracted_data['symptoms'] = symptoms
    if len(diseases):
        extracted_data['diseases'] = diseases
    if len(diagnostics):
        extracted_data['diagnostics'] = diagnostics

    return extracted_data
