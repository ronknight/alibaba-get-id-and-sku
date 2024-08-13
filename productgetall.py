import os
import requests
import hashlib
import time
import json
import csv
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
session_key = os.getenv('SESSION_KEY')

# Define the log directory
LOG_DIR = 'api_logs/'  # Directory to store log files
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if it doesn't exist

# API endpoint
url = 'https://eco.taobao.com/router/rest'

# Path to the CSV file containing product IDs
csv_file_path = 'alibaba_product_id.csv'

# Output JSON file path
combined_log_file = f"{LOG_DIR}combined_productget_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

# Initialize a list to hold all responses
combined_responses = []

# Calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Remove sensitive information for logging
def remove_sensitive_info(params):
    safe_params = params.copy()
    safe_params.pop('app_key', None)
    safe_params.pop('session', None)
    safe_params.pop('sign', None)
    return safe_params

# Read product IDs from CSV and make API requests with a progress bar
with open(csv_file_path, newline='') as csvfile:
    csv_reader = list(csv.DictReader(csvfile))  # Convert reader to list for length calculation
    total_products = len(csv_reader)
    
    # Initialize tqdm progress bar with a single line
    with tqdm(total=total_products, desc="Processing Product IDs", ncols=100, ascii=True) as pbar:
        for row in csv_reader:
            product_id = row['Alibaba Product ID']

            params = {
                'app_key': app_key,
                'format': 'json',
                'method': 'alibaba.icbu.product.get',
                'partner_id': 'apidoc',
                'session': session_key,
                'sign_method': 'md5',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'v': '2.0',
                'language': 'ENGLISH',  # Set language to English
                'product_id': product_id,  # Product ID from the CSV file
            }

            # Add sign to parameters
            params['sign'] = calculate_sign(params, app_secret)

            try:
                # Make the API request
                get_product_request = requests.get(url, params=params)
                get_product_response = get_product_request.json()

                # Store the response data in the combined_responses list
                combined_responses.append({
                    'product_id': product_id,
                    'request_params': remove_sensitive_info(params),
                    'response': get_product_response,
                })

                # Check for error responses
                if get_product_response.get('error_response'):
                    # Add error response to combined_responses
                    combined_responses.append({
                        'product_id': product_id,
                        'request_params': remove_sensitive_info(params),
                        'error_message': get_product_response['error_response']['msg'],
                    })

            except requests.exceptions.RequestException as e:
                # Store the error in the combined_responses list
                combined_responses.append({
                    'product_id': product_id,
                    'request_params': remove_sensitive_info(params),
                    'error_message': str(e),
                })

            # Update the progress bar in the same line
            pbar.update(1)

# Write the combined responses to a single JSON file
with open(combined_log_file, 'w') as f:
    json.dump(combined_responses, f, indent=4)

print(f"All API responses have been saved to {combined_log_file}.")
