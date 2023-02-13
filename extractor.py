import os
import zipfile
from PyPDF3 import PdfFileMerger
import shutil

folder = "2023 Winter"
for item in os.listdir(folder):
    print("Working on " + item)
    path = folder + "\\" + item.split(".")[0]
    with zipfile.ZipFile(folder + "\\" + str(item), "r") as zip_ref:

        zip_ref.extractall(path)

    merger = PdfFileMerger()
    # print("here")
    for it in os.listdir(path):
        print("Merging file ", it)
        merger.append(path + "\\" + it)
    merger.write(path + ".pdf")
    merger.close()
    os.remove(path + ".zip")
    shutil.rmtree(path)
