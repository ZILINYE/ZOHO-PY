import requests
from tqdm import tqdm



token = "1000.2d7cd1a6d206633bb3a67775c3a6fd8d.4fa07f006931def905ed8a1cc88fe51a"
url = "https://sign.zoho.com/api/v1/requests"
headers = {
        "Authorization": "Zoho-oauthtoken "+ token,
    }
r = requests.get(url+"/"+'130808000003585129'+"/pdf",headers=headers,stream=True)
total_size_in_bytes= int(r.headers.get('content-length', 0))
block_size = 1024 #1 Kibibyte
progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
with open('test.zip',"wb") as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            progress_bar.update(len(chunk))
            f.write(chunk)