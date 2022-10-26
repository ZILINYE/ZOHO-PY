from email import header
import threading
from wsgiref.util import request_uri
from black import parse_ast
import requests
import json
from maria import Maria
from tqdm import tqdm
from queue import Queue

exitFlag=0
studentInfo = Maria()
token = "1000.7549631639bff8a3639c3431d917dd61.7e9e2a0d8cb66add3cebc14d50b4ef74"
url = "https://sign.zoho.com/api/v1/requests"
headers = {
        "Authorization": "Zoho-oauthtoken "+ token
    }

queueLock = threading.Lock()

DownloadList = Queue(1200)
threads=[]
class myThread (threading.Thread):
    def __init__(self,threadID,q):
        threading.Thread.__init__(self)
        self.threadID = threadID

        self.q = q
    def run(self):
        print("starting thread "+str(self.threadID))
        getDownloadPDF(self.q)
        print("finished thread "+str(self.threadID))
        
        


    
    
    
    
# grab document list from the API that mathch the search 
def getDocumentList(start_index) -> list:
    params = {
        "data" : '{"page_context": {"row_count": 10, "start_index": '+str(start_index)+', "search_columns": {"request_name": "22F"}, "sort_column": "created_time", "sort_order": "DESC"}}'
    }
    r = requests.get(url, headers=headers, params=params).json()

    outputlist = []
    documentlist = r['requests']
    for item in documentlist:
        if item['request_status'] == 'completed':
            
            campemail = item['actions'][0]['recipient_email']
            
            fileprefix = item['document_ids'][0]['document_name'][:9]
            
            request_id = item['request_id']
            
            studentID = getStudentInfo(campemail=campemail)
            if studentID:

                outputlist.append([fileprefix,request_id,studentID])
            else:
                print('%s email not found in Database' % campemail)
                
    # print(len(outputlist))
    # print(outputlist)
    return outputlist
    


# Get student information from database
def getStudentInfo(campemail) -> str:
    studentID = studentInfo.GetStudentInfo(campemail=campemail)
    return studentID
    
# Download zip file
def getDownloadPDF(q):
    while not exitFlag:
        
        if not DownloadList.empty():
            queueLock.acquire()
            data = q.get()
            queueLock.release()
            fileprefix=data[0]
            request_id = data[1]
            student_id = data[2]
            # print(data)
            r = requests.get(url+"/"+request_id+"/pdf",headers=headers,stream=True)
            total_size_in_bytes= int(r.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(fileprefix+student_id+'.zip',"wb") as f:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:  # filter out keep-alive new chunks
                        progress_bar.update(len(chunk))
                        f.write(chunk)
            progress_bar.close()
        

thread_number = 2
thread_index = 1
start_index = 1

while thread_index <= thread_number:
    thread = myThread(thread_index,DownloadList)
    thread.start()
    threads.append(thread)
    thread_index +=1



i = 1
while i <= thread_number:
    
    pageList = getDocumentList(start_index)
    for item in pageList:
        DownloadList.put(item)
    start_index += 10
    i+=1
# DownloadList.get()
while not DownloadList.empty():
    pass

for t in threads:
    t.join()
print("exit the thread!!")
