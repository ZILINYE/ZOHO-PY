import os
for item in os.listdir("wait"):
    with zipfile.ZipFile(item, 'r') as zip_ref:
        zip_ref.extractall(filename)
        merger = PdfMerger()
        for it in os.listdir(item.split(".")[0])
            merger.append(item.split(".")[0]+"\\"+it)
                merger.write(filename+".pdf")
        merger.close()