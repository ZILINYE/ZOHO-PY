import threading
import requests
import json
from maria import Maria
from tqdm import tqdm
from queue import Queue
import math
import zipfile
import os
from PyPDF2 import PdfMerger
import shutil
import pandas as pd 


def GetAccessToken():
    r = requests.post(url="https://accounts.zoho.com/oauth/v2/token?refresh_token=1000.23be290456580cd7378b94f2eb3d2334.8ed115d741371a6cf5ada13b2903819e&client_id=1000.6C4D4C3LQS1XV9BVF70PS55G3PELTK&client_secret=211e6b7d3395fd9e8f7d67df464a884e0f573c6079&redirect_uri=https%3A%2F%2Fsign.zoho.com&grant_type=refresh_token")
    access_token = r.json()['access_token']
    return access_token


exitFlag = 0
studentInfo = Maria()
term = "Winter"
year = 2020
search_key = "Winter 2020"
token = GetAccessToken()
url = "https://sign.zoho.com/api/v1/requests"
headers = {
    "Authorization": "Zoho-oauthtoken " + token,
}
row_count = 10



def HttpRequest(start_index):
    params = {
        "data": '{"page_context": {"row_count":'+str(row_count)+' , "start_index": '+str(start_index)+', "search_columns": {"request_name": '+ search_key +'}, "sort_column": "created_time", "sort_order": "DESC"}}'
    }
    r = requests.get(url, headers=headers, params=params).json()
    return r


qsize = HttpRequest(1)['page_context']['total_count']
queueLock = threading.Lock()
DownloadList = Queue(qsize)
ExtractList = Queue(qsize)
thread_number = math.ceil(qsize/row_count)  # Page number 
# thread_number = 2
class myThread (threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID

        self.q = q

    def run(self):
        print("starting thread "+str(self.threadID))
        pdfProcess(self.q)
        print("finished thread "+str(self.threadID))


# grab document list from the API that mathch the search
def getDocumentList(start_index) -> list:

    outputlist = []
    documentlist = HttpRequest(start_index)['requests']
    for item in documentlist:
        if item['request_status'] == 'completed':

            campemail = item['actions'][0]['recipient_email']

            # fileprefix = item['document_ids'][0]['document_name'][:9]
            # term = "Spring"
            # year = 2022
            
            request_id = item['request_id']

            studentID,program = getStudentInfo(year,term,campemail)
            if studentID:
                fileprefix = str(year) + "-" + term + "-"+program+"-"
                outputlist.append([fileprefix, request_id, studentID])
                downloadList = open("DownloadList.txt", "a")
                downloadList.write(fileprefix+' '+str(request_id)+' '+studentID+'\n')
                downloadList.close()
            else:
                f = open("misslist.txt", "a")
                f.write(campemail+'\n')
                f.close()

    return outputlist


# Get student information from database
def getStudentInfo(year,term,campemail):
    studentID,program = studentInfo.GetStudentInfo(year,term,campemail)
    return studentID,program

# Download zip file


def getDownloadPDF(q):

    fileprefix = q[0]
    request_id = q[1]
    student_id = q[2]

    r = requests.get(url+"/"+request_id+"/pdf", headers=headers, stream=False)
    total_size_in_bytes = int(r.headers.get('content-length', 0))

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    zipfilename = fileprefix+student_id
    with open(zipfilename+'.zip', "wb") as f:
        for chunk in r.iter_content(chunk_size=10240):
            if chunk:  # filter out keep-alive new chunks
                progress_bar.update(len(chunk))
                f.write(chunk)
    progress_bar.close()
    ExtractList.put(zipfilename)


def pdfProcess(q):

    if not ExtractList.empty():
        # queueLock.acquire()
        filename = q.get()
        
        with zipfile.ZipFile(filename+'.zip', 'r') as zip_ref:
            zip_ref.extractall(filename)
        merger = PdfMerger()
        for item in os.listdir(filename):
            merger.append(filename+"\\"+item)
        merger.write(filename+".pdf")
        merger.close()
        #  Delete old zip file and folder
        os.remove(filename+'.zip')
        shutil.rmtree(filename)
        # queueLock.release()


def main():

    threads = []

    thread_index = 1
    start_index = 1

        
    dlist = []
    i = 1
    while i <= thread_number:

        pageList = getDocumentList(start_index)
        # df = pd.DataFrame(pageList)
        # df.to_csv('test.csv',mode='a',index=False,header=False)
        # print(df)
        for item in pageList:
            dlist.append(item)
        start_index += 10
        i += 1
    # for item in dlist:
    #     getDownloadPDF(item)

    # while not ExtractList.empty():
    #     pdfProcess(ExtractList)
    # while thread_index <= thread_number:
    #     thread = myThread(thread_index, ExtractList)
    #     thread.start()
    #     threads.append(thread)
    #     thread_index += 1


    # exitFlag = 1
    # for t in threads:
    #     t.join()
    print("exit the thread!!")


main()
