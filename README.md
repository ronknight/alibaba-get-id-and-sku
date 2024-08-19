<h1 align="center">🛒 <a href="https://github.com/ronknight/alibaba-get-id-and-sku">Alibaba Get ID and SKU</a></h1>

<h4 align="center">🐍 A Python script to fetch product IDs and SKUs from Alibaba's API and parse the results 📊</h4>

<p align="center">
<a href="https://twitter.com/PinoyITSolution"><img src="https://img.shields.io/twitter/follow/PinoyITSolution?style=social"></a>
<a href="https://github.com/ronknight?tab=followers"><img src="https://img.shields.io/github/followers/ronknight?style=social"></a>
<a href="https://github.com/ronknight/ronknight/stargazers"><img src="https://img.shields.io/github/stars/BEPb/BEPb.svg?logo=github"></a>
<a href="https://github.com/ronknight/ronknight/network/members"><img src="https://img.shields.io/github/forks/BEPb/BEPb.svg?color=blue&logo=github"></a>
<a href="https://youtube.com/@PinoyITSolution"><img src="https://img.shields.io/youtube/channel/subscribers/UCeoETAlg3skyMcQPqr97omg"></a>
<a href="https://github.com/ronknight/alibaba-get-id-and-sku/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
<a href="https://github.com/ronknight/alibaba-get-id-and-sku/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
<a href="#"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
<a href="https://github.com/ronknight"><img src="https://img.shields.io/badge/Made%20with%20%F0%9F%A4%8D%20by%20-%20Ronknight%20-%20red"></a>
</p>

<p align="center">
<a href="#requirements">Requirements</a> • 
<a href="#installation">Installation</a> • 
<a href="#usage">Usage</a> • 
<a href="#script-details">Script Details</a> • 
<a href="#diagrams">Diagrams</a> •
<a href="#disclaimer">Disclaimer</a>
</p>

---

## 🛠️ Requirements

- Python 3.6+
- `requests` library
- `python-dotenv` library

## 📥 Installation

1. Clone the repository:
   ```
   git clone https://github.com/ronknight/alibaba-get-id-and-sku.git
   ```

2. Navigate to the project directory:
   ```
   cd alibaba-get-id-and-sku
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Alibaba API credentials:
   ```
   APP_KEY=your_app_key
   APP_SECRET=your_app_secret
   SESSION_KEY=your_session_key
   ```

## 🚀 Usage

1. Run the main script:

```
python main.py
```

This will execute both `productlist.py` and `parse_id_sku.py` in sequence.

2. Run the productgetall script:

```
python productgetall.py
```
This will processes product IDs from a CSV file and create a JSON file with all product info.

3. Run the extract_not_updated_sku script:

```
python extract_not_updated_sku.py
```
This will identify which SKU is still not updated.


## 📜 Script Details

### 1. productlist.py

🔍 This script fetches product information from the Alibaba API:

- Sends requests to the Alibaba API endpoint
- Retrieves product data page by page
- Logs both request and response data

### 2. parse_id_sku.py

📊 This script processes the API response logs:

- Extracts product IDs and SKUs from the logged responses
- Writes the extracted data to a CSV file (`product_id.csv`)

### 3. main.py

🔄 This is the main orchestrator script:

- Runs `productlist.py` to fetch data from the API
- Runs `parse_id_sku.py` to process the fetched data

### 4. productgetall.py

🚀 Fetches detailed product information for each product ID in the CSV file using the Alibaba API.

- Processes product IDs from a CSV file
- Saves all API responses and errors to a single JSON file with a progress bar display

### 5. extract_product_id.py

📊 Extracts product IDs, SKUs, and Alibaba product IDs from API response logs and saves them to a CSV file.

- Parses API log data to extract product information using regex and JSON processing
- Outputs a CSV file with SKUs, Product IDs, and Alibaba Product IDs for further analysis


### 6. extract_not_updated_sku.py

🔍 Identifies product IDs from API logs that are not present in the Alibaba product CSV file.

- Compares product IDs from the latest JSON log file against those in the Alibaba CSV
- Outputs a new CSV file containing product IDs found in the log but missing from the Alibaba data

<!-- eraser-additional-content -->
## 📊 Diagrams

### Program Flow

The program flow can be visualized as follows:

1. Start
2. main.py is executed
3. main.py runs productlist.py
4. productlist.py fetches data from Alibaba API
5. API responses are logged
6. main.py runs productgetall.py
7. productgetall.py fetches detailed product information for each product ID
8. main.py runs extract_product_id.py
9. extract_product_id.py extracts product IDs, SKUs, and Alibaba product IDs from logs
10. main.py runs parse_id_sku.py
11. parse_id_sku.py processes the fetched data
12. Extracted data is written to CSV files
13. main.py runs extract_not_updated_sku.py
14. extract_not_updated_sku.py identifies not updated product IDs
15. End

### Data Flow

The data flow can be represented as:

1. Alibaba API (source of data)
2. Data flows to productlist.py
3. productlist.py generates API response logs
4. productgetall.py fetches detailed product information
5. extract_product_id.py processes logs and outputs to alibaba_product_id.csv
6. parse_id_sku.py processes data and outputs to product_id.csv
7. extract_not_updated_sku.py compares data and outputs to not_updated_product_ids.csv

<!-- eraser-additional-files -->
<a href="/README-Alibaba Get ID and SKU Flowchart-1.eraserdiagram" data-element-id="XTttFq5zD5Bo2v358sPiq"><img src="/.eraser/53LCLwpB7TEuHVz5qGu6___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----aca7057b97d8c375d6333da24af24a33-Alibaba-Get-ID-and-SKU-Flowchart.png" alt="" data-element-id="XTttFq5zD5Bo2v358sPiq" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/53LCLwpB7TEuHVz5qGu6 --->

## ⚠️ Disclaimer

This script is for educational purposes only. Ensure you have the necessary permissions and comply with Alibaba's terms of service when using their API.

---

Feel free to contribute to this project by opening issues or submitting pull requests!