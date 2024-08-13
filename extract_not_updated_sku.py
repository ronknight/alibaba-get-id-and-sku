import os
import json
import csv
from datetime import datetime

# Define the directory containing the log files
log_directory = 'api_logs/'

# Path to the CSV file with Alibaba product IDs
alibaba_product_csv = 'alibaba_product_id.csv'

# Function to find the latest JSON log file in the directory based on timestamp
def find_latest_log_file(directory):
    files = [f for f in os.listdir(directory) if f.startswith('combined_productget_logs_') and f.endswith('.json')]
    if not files:
        raise FileNotFoundError("No JSON log files found in the directory.")
    
    # Extract timestamp from filenames and find the most recent one
    def extract_timestamp(filename):
        timestamp_str = filename[len('combined_productget_logs_'): -len('.json')]
        return datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
    
    latest_file = max(files, key=lambda f: extract_timestamp(f))
    return os.path.join(directory, latest_file)

# Initialize a set to hold product IDs from the latest log file
product_ids_from_log = set()

# Function to recursively search for product IDs in the JSON data
def find_product_ids(data):
    if isinstance(data, dict):
        # Check for product ID attributes
        if data.get('attribute_name') == 'PRD_ID':
            product_ids_from_log.add(data.get('value_name'))
        for key, value in data.items():
            find_product_ids(value)
    elif isinstance(data, list):
        for item in data:
            find_product_ids(item)

# Read Alibaba product IDs from CSV file
def read_alibaba_product_ids(csv_file):
    alibaba_product_ids = set()
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'Alibaba Product ID' not in reader.fieldnames:
            raise KeyError("Column 'Alibaba Product ID' not found in CSV file.")
        for row in reader:
            alibaba_product_ids.add(row['Alibaba Product ID'])
    return alibaba_product_ids

# Load the latest log file
try:
    latest_log_file = find_latest_log_file(log_directory)
    print(f"Latest log file found: {latest_log_file}")
except FileNotFoundError as e:
    print(e)
    exit()

with open(latest_log_file, 'r') as file:
    try:
        data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        exit()

# Extract product IDs from the log file
find_product_ids(data)
print(f"Product IDs extracted from log file: {product_ids_from_log}")

# Read Alibaba product IDs
try:
    alibaba_product_ids = read_alibaba_product_ids(alibaba_product_csv)
    print(f"Alibaba Product IDs from CSV: {alibaba_product_ids}")
except FileNotFoundError as e:
    print(e)
    exit()
except KeyError as e:
    print(e)
    exit()

# Determine which product IDs from the log file are not in the Alibaba product IDs
not_updated_product_ids = [product_id for product_id in product_ids_from_log if product_id not in alibaba_product_ids]
print(f"Not updated product IDs: {not_updated_product_ids}")

# Write the not updated product IDs to a CSV file
output_csv_file = 'not_updated_product_ids.csv'
with open(output_csv_file, 'w', newline='') as csvfile:
    fieldnames = ['product_id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for product_id in not_updated_product_ids:
        writer.writerow({'product_id': product_id})

print(f"Not updated product IDs have been written to {output_csv_file}.")
