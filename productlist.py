import os
import sys
import requests
import hashlib
import time
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
session_key = os.getenv('SESSION_KEY')

# Command-line arguments
if len(sys.argv) != 3 or sys.argv[1] not in ['10', '20', '30']:
    print("Usage: productlist.py <page_size> <start_page>")
    print("Page size options: 10, 20, 30")
    sys.exit(1)

page_size = sys.argv[1]
start_page = int(sys.argv[2])

# API endpoint
url = 'https://eco.taobao.com/router/rest'

def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

def fetch_products(page_number):
    params = {
        'app_key': app_key,
        'format': 'json',
        'method': 'alibaba.icbu.product.list',
        'partner_id': 'apidoc',
        'session': session_key,
        'sign_method': 'md5',
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'v': '2.0',
        'current_page': page_number,
        'page_size': page_size,
        'language': 'ENGLISH',
    }
    params['sign'] = calculate_sign(params, app_secret)

    response = requests.post(url, data=params)
    response_data = response.json()

    # Log request and response
    log_dir = 'api_logs'
    os.makedirs(log_dir, exist_ok=True)

    # Log request details
    request_time = time.strftime("%Y-%m-%d %H:%M:%S")
    productlist_request_log = {
        "Request Time": request_time,
        "Request URL": url,
        "Request Method": "POST",
        "Request Headers": {k: v for k, v in params.items() if k not in ['app_key', 'session', 'sign']}
    }
    with open(os.path.join(log_dir, 'productlist_request_log.txt'), 'a') as f:
        f.write(json.dumps(productlist_request_log, indent=4) + "\n\n")

    # Log response details
    response_time = time.strftime("%Y-%m-%d %H:%M:%S")
    productlist_response_log = {
        "Response Time": response_time,
        "Response Status Code": response.status_code,
        "Response Headers": dict(response.headers),
        "Response Body": response.text
    }
    with open(os.path.join(log_dir, 'productlist_response_log.txt'), 'a') as f:
        f.write(json.dumps(productlist_response_log, indent=4) + "\n\n")

    return response_data

def main():
    page_number = start_page
    while True:
        print(f"Fetching products from page {page_number}...")
        response_data = fetch_products(page_number)

        if 'alibaba_icbu_product_list_response' in response_data:
            product_list_response = response_data['alibaba_icbu_product_list_response']
            products = product_list_response.get('products', {}).get('alibaba_product_brief_response', [])

            if not products:
                print(f"No more products found on page {page_number}. Stopping.")
                break

            for product in products:
                if isinstance(product, dict):
                    subject = product.get('subject', '')
                    print(f"Product Subject: {subject}")
                else:
                    print("Invalid product structure.")

            page_number += 1
        else:
            print("Unexpected JSON structure: alibaba_icbu_product_list_response not found.")
            break

if __name__ == "__main__":
    main()
