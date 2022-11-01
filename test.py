import zipfile
with zipfile.ZipFile('test.zip', 'r') as zip_ref:
    zip_ref.extractall('test')