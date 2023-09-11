  # Project README - EPWK Data Scraper

## Project Overview
This project aims to extract email and phone contact information from users registered at https://talent.epwk.com/wuxian/, a platform that caters to app development professionals. A "user" here can refer to an individual or an organization/company.

## Directory Structure
- **thief\src\workflow** - Contains the main workflow scripts.
- **thief\src\work_flow_io** - Directory for storing input and output files.
- **thief\src\utils** - Contains utility methods and helper functions.
- **thief\src\excels** - Storage for test Excel files.

## Workflow Steps
1. **Nickname Extraction** (`scrapeShopName.py`)
   - Scrapes the nickname displayed on the top banner from EPWK.
   - Saves the scraped nickname and the corresponding website's URL locally.

2. **Company URL Extraction** (`findCompanyUrl.py`)
   - Uses the scraped nickname to search on www.tianyacha.com, an official site for company searches.
   - Confirms the company's identity by matching the nickname from EPWK with the one on Tianyacha.
   - This step helps minimize the load on the subsequent OCR process.

3. **Trust Image Extraction** (`findTrust.py`)
   - For unrecognized entries, revisit the original EPWK URL.
   - Downloads the images of the 'Business Licence of Legal Entity' (a requirement for registration on EPWK).
   - Saves these images locally. *Note: Due to storage constraints, the downloaded images from `thief\src\work_flow_io\trust` are deleted post-process*.

4. **OCR Analysis** (`BDImageDetect.py`)
   - Uses an access token and a secret key to tap into Baidu's OCR API.
   - Analyzes the images to extract unique registration numbers.
   - Repeats the company search on Tianyacha but uses the unique registration number as the keyword.

5. **Contact Information Extraction** (`findEmailandPhone.py`)
   - After obtaining the official company name and associated URLs on both https://www.tianyacha.com and https://www.epwk.com, this script scrapes the email and phone contact details.
   - All gathered data is compiled into a single Excel output file.

## Conclusion
This scraper efficiently traverses through the EPWK platform, confirming identities through Tianyacha and ultimately gleaning important contact data. It's a multi-step process ensuring data accuracy and minimal reliance on the OCR step which incurs additional costs.

---
