import os
import base64
import urllib
import requests
import pandas as pd


API_KEY = ""
SECRET_KEY = ""


def get_file_content_as_base64(path, urlencoded=False):
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def process_image(file_path):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license?access_token=" + get_access_token()

    payload = 'image=' + get_file_content_as_base64(file_path, True)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()  # return as json to easily convert to DataFrame later


if __name__ == '__main__':
    folder_path = "../work_flow_io/trust_filtered"
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('.jpg', '.png', '.jpeg'))]
    image_files = image_files[850:]
    output = 1;
    results = []
    for image_file in image_files:
        full_path = os.path.join(folder_path, image_file)
        print("Getting to Image: ", output)
        output += 1
        result = process_image(full_path)
        if 'words_result' in result and '社会信用代码' in result['words_result']:
            # Extract the 'words' part for '社会信用代码' from result
            social_credit_code = result['words_result']['社会信用代码']['words']
            results.append({'file_name': image_file, '社会信用代码': social_credit_code})
        else:
            print(f"No 'words_result' or '社会信用代码' found in image: {image_file}. Skipping this image.")

    df = pd.DataFrame(results)
    df.to_excel('../work_flow_io/results1.xlsx', index=False)

