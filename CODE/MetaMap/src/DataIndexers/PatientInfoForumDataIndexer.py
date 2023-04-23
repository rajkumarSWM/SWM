import requests
import os
import json
import time

from src.MetaMap import MetaMap

CURRENT_DIR = os.path.dirname(__file__)

# Set the range of data to be indexed
start_index = 12000
end_index = 13500

# Helper function to remove non-ASCII characters from text
def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

# Function to index JSON file
def index_json_file(file_path):
    mmw = MetaMapWrapper()

    # Open the JSON file
    with open(file_path) as json_file:
        data = json.load(json_file)
        failed_count = 0
        i = 0
        
        # Loop through the posts in the JSON file
        for post in data:
            # Skip posts that are outside of the desired range
            i += 1
            if i < start_index or i > end_index:
                continue
            
            # Skip posts that don't meet the specified criteria
            if i % 3 != 0:
                continue

            # Wait for a short time before making the request
            # time.sleep(0.25)
            
            try:
                preprocessed_post = {}
                text_to_annotate = ''
                
                # Add the post data to the preprocessed_post dictionary
                preprocessed_post['post_group'] = post['post_group']
                preprocessed_post['post_url'] = post['post_url']
                preprocessed_post['post_title'] = post['post_title']
                text_to_annotate += post['post_title']
                preprocessed_post['post_time'] = post['post_time']
                preprocessed_post['post_follow_count'] = post['post_follow_count']
                preprocessed_post['post_author'] = post['post_author']
                preprocessed_post['post_author_profile'] = post['post_author_profile']
                preprocessed_post['post_like_count'] = post['post_like_count']
                preprocessed_post['post_reply_count'] = post['post_reply_count']
                preprocessed_post['post_content'] = post['post_content']
                text_to_annotate += ' ' + post['post_content']

                # Add the comments data to the preprocessed_post dictionary
                comments = ''
                if 'post_comments' in post:
                    post_comments = post['post_comments']
                    for comment in post_comments:
                        comment_content = comment['comment_content']
                        comment_content = comment_content.replace("\n", " ")
                        comments += ' ' + comment_content
                    text_to_annotate += ' ' + comments
                preprocessed_post['post_comments'] = comments
                
                # Call MetaMap to extract medical terms from the text
                if len(text_to_annotate) > 0:
                    # Remove non-ASCII characters to avoid tagging issues
                    text_to_annotate = remove_non_ascii(text_to_annotate)
                    extracted_data = mmw.annotate(text_to_annotate)

                    # Add the extracted medical terms to the preprocessed_post dictionary
                    if 'symptoms' in extracted_data:
                        preprocessed_post['symptoms'] = extracted_data['symptoms']
                    if 'diseases' in extracted_data:
                        preprocessed_post['diseases'] = extracted_data['diseases']
                    if 'diagnostics' in extracted_data:
                        preprocessed_post['diagnostic_procedures'] = extracted_data['diagnostics']

                # Send the preprocessed_post data to the server
                r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "patient_info"},
                                  json=preprocessed_post)

if __name__ == "__main__":
    # alternatively pass the path of crawled data file
    index_json_file(CURRENT_DIR + os.path.sep + "patient_info_forum_posts_content-1.json")
    # index_json_file(CURRENT_DIR + os.path.sep + "patient_info_forum_posts_content-2.json")
