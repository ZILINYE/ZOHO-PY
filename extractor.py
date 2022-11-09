import os
import zipfile
from PyPDF2 import PdfMerger
import shutil

folder = "2020 Fall"
for item in os.listdir(folder):
    print("Working on "+item)
    path = folder+"\\"+item.split(".")[0]
    with zipfile.ZipFile(folder+"\\"+str(item), 'r') as zip_ref:
   
        zip_ref.extractall(path)
    merger = PdfMerger()
    for it in os.listdir(path):
        merger.append(path+"\\"+it)
    merger.write(path+".pdf")
    merger.close()
    os.remove(path+'.zip')
    shutil.rmtree(path)
