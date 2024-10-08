import os
import json
import csv
import re

# Define file paths
log_file_path = 'api_logs/productlist_response_log.txt'
csv_file_path = 'alibaba_product_id.csv'

# Function to extract last 14 digits from URLs before '.html'
def extract_product_ids(text):
    # Regular expression to match URLs with 14 digits before '.html'
    pattern = re.compile(r'(\d{14})\.html')
    return pattern.findall(text)

# Function to extract red_model from response body
def extract_red_model(text):
    try:
        data = json.loads(text)
        products = data.get('alibaba_icbu_product_list_response', {}).get('products', {}).get('alibaba_product_brief_response', [])
        return [product.get('red_model', '') for product in products if isinstance(product, dict)]
    except json.JSONDecodeError:
        return []

# Function to extract Alibaba product_id from response body
def extract_alibaba_product_id(text):
    try:
        data = json.loads(text)
        products = data.get('alibaba_icbu_product_list_response', {}).get('products', {}).get('alibaba_product_brief_response', [])
        return [product.get('product_id', '') for product in products if isinstance(product, dict)]
    except json.JSONDecodeError:
        return []

# Ensure log file exists
if not os.path.exists(log_file_path):
    print(f"Log file not found: {log_file_path}")
    exit(1)

# Create or clear the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['4SGM_SKU', 'Product ID', 'Alibaba Product ID'])  # Write header

    # Read the log file
    with open(log_file_path, 'r') as logfile:
        buffer = ''
        for line in logfile:
            buffer += line.strip()
            # Try to parse JSON when the buffer contains a complete object
            try:
                while buffer:
                    data, index = json.JSONDecoder().raw_decode(buffer)
                    buffer = buffer[index:].lstrip()

                    # Extract red_model, product IDs, and Alibaba product IDs
                    response_body = data.get('Response Body', '')
                    red_models = extract_red_model(response_body)
                    alibaba_product_ids = extract_alibaba_product_id(response_body)
                    product_ids = extract_product_ids(response_body)

                    # Ensure we have matching red_models, product_ids, and alibaba_product_ids
                    for red_model, product_id, alibaba_product_id in zip(red_models, product_ids, alibaba_product_ids):
                        csv_writer.writerow([red_model, product_id, alibaba_product_id])
            except json.JSONDecodeError:
                continue

print(f"Data has been extracted to {csv_file_path}.")
