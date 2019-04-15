import argparse
import os
from werkzeug import secure_filename
from flask import Flask, render_template, request
from time import sleep
import time
import sys
import json
from flask import Flask

app = Flask(__name__)

#Server info
HOST_IP = "0.0.0.0"
HOST_PORT = 2222

SFTP_PORT = 1022
FTPS_PORT = 21

#Test function to check server running
@app.route('/',
    methods=['GET'])
def index():
    return 'Hello world'

#Returns number of polls
@app.route('/ctr_requests',
    methods=['GET'])
def counter_requests():
    global ctr_requests
    return str(ctr_requests)

#Returns number of replies
@app.route('/ctr_responses',
    methods=['GET'])
def counter_responses():
    global ctr_responses
    return str(ctr_responses)

#Returns number of unique files
@app.route('/ctr_unique_files',
    methods=['GET'])
def counter_uniquefiles():
    global fileMap
    return str(len(fileMap))

#Returns tc info
@app.route('/tc_info',
    methods=['GET'])
def testcase_info():
    global tc_num
    return tc_num

#Returns number of events
@app.route('/ctr_events',
    methods=['GET'])
def counter_events():
    global ctr_events
    return str(ctr_events)

#Returns number of events
@app.route('/execution_time',
    methods=['GET'])
def exe_time():
    global startTime
    
    stopTime = time.time()
    minutes, seconds = divmod(stopTime-startTime, 60)
    return "{:0>2}:{:0>2}".format(int(minutes),int(seconds))

#Returns number of unique PNFs
@app.route('/ctr_unique_PNFs',
    methods=['GET'])
def counter_uniquePNFs():
    global pnfMap
    return str(len(pnfMap))

#Messages polling function
@app.route(
    "/events/unauthenticated.VES_NOTIFICATION_OUTPUT/OpenDcae-c12/C12",
    methods=['GET'])
def MR_reply():
    global ctr_requests
    global args

    ctr_requests = ctr_requests + 1
    print("MR: poll request#: " + str(ctr_requests))

    if args.tc100:
      return tc100("sftp")
    elif args.tc101:
      return tc101("sftp")
    elif args.tc102:
      return tc102("sftp")

    elif args.tc110:
      return tc110("sftp")
    elif args.tc111:
      return tc111("sftp")
    elif args.tc112:
      return tc112("sftp")
    elif args.tc113:
      return tc113("sftp")

    elif args.tc120:
      return tc120("sftp")
    elif args.tc121:
      return tc121("sftp")
    elif args.tc122:
      return tc122("sftp")

    elif args.tc1000:
      return tc1000("sftp")
    elif args.tc1001:
      return tc1001("sftp")

    elif args.tc510:
      return tc510("sftp")  
    elif args.tc511:
      return tc511("sftp")   
  
    elif args.tc710:
      return tc710("sftp")     


    elif args.tc200:
      return tc200("ftps")
    elif args.tc201:
      return tc201("ftps")
    elif args.tc202:
      return tc202("ftps")

    elif args.tc210:
      return tc210("ftps")
    elif args.tc211:
      return tc211("ftps")
    elif args.tc212:
      return tc212("ftps")
    elif args.tc213:
      return tc213("ftps")

    elif args.tc220:
      return tc220("ftps")
    elif args.tc221:
      return tc221("ftps")
    elif args.tc222:
      return tc222("ftps")

    elif args.tc2000:
      return tc2000("ftps")
    elif args.tc2001:
      return tc2001("ftps")

    elif args.tc610:
      return tc510("ftps")  
    elif args.tc611:
      return tc511("ftps") 
  
    elif args.tc810:
      return tc710("ftps")   


#### Test case functions


def tc100(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 1):
    return buildOkResponse("[]")

  seqNr = (ctr_responses-1)
  nodeName = createNodeName(0)
  fileName = createFileName(nodeName, seqNr, "1MB")
  msg = getEventHead(nodeName) + getEventName(fileName,ftptype,"onap","pano") + getEventEnd()
  fileMap[seqNr] = seqNr
  ctr_events = ctr_events+1
  return buildOkResponse("["+msg+"]")

def tc101(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 1):
    return buildOkResponse("[]")  

  seqNr = (ctr_responses-1)
  nodeName = createNodeName(0)
  fileName = createFileName(nodeName, seqNr, "5MB")
  msg = getEventHead(nodeName) + getEventName(fileName,ftptype,"onap","pano") + getEventEnd()
  fileMap[seqNr] = seqNr
  ctr_events = ctr_events+1
  return buildOkResponse("["+msg+"]")

def tc102(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 1):
    return buildOkResponse("[]")  

  seqNr = (ctr_responses-1)
  nodeName = createNodeName(0)
  fileName = createFileName(nodeName, seqNr, "50MB")
  msg = getEventHead(nodeName) + getEventName(fileName,ftptype,"onap","pano") + getEventEnd()
  fileMap[seqNr] = seqNr
  ctr_events = ctr_events+1
  return buildOkResponse("["+msg+"]")

def tc110(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 100):
    return buildOkResponse("[]")  
  
  seqNr = (ctr_responses-1)
  nodeName = createNodeName(0)
  fileName = createFileName(nodeName, seqNr, "1MB")
  msg = getEventHead(nodeName) + getEventName(fileName,ftptype,"onap","pano") + getEventEnd()
  fileMap[seqNr] = seqNr
  ctr_events = ctr_events+1
  return buildOkResponse("["+msg+"]")

def tc111(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 100):
    return buildOkResponse("[]")  

  nodeName = createNodeName(0)
  msg = getEventHead(nodeName)

  for i in range(100):
    seqNr = i+(ctr_responses-1)
    if i != 0: msg = msg + ","
    fileName = createFileName(nodeName, seqNr, "1MB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    fileMap[seqNr] = seqNr

  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc112(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 100):
    return buildOkResponse("[]")  

  nodeName = createNodeName(0)
  msg = getEventHead(nodeName)

  for i in range(100):
    seqNr = i+(ctr_responses-1)
    if i != 0: msg = msg + ","
    fileName = createFileName(nodeName, seqNr, "5MB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    fileMap[seqNr] = seqNr

  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc113(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 1):
    return buildOkResponse("[]")  

  nodeName = createNodeName(0)
  msg = ""

  for evts in range(100):  # build 100 evts
    if (evts > 0):
      msg = msg + ","
    msg = msg + getEventHead(nodeName)
    for i in range(100):   # build 100 files
      seqNr = i+evts+100*(ctr_responses-1)
      if i != 0: msg = msg + ","
      fileName = createFileName(nodeName, seqNr, "1MB")
      msg = msg + getEventName(fileName,ftptype,"onap","pano")
      fileMap[seqNr] = seqNr

    msg = msg + getEventEnd()
    ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")


def tc120(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  nodeName = createNodeName(0)

  if (ctr_responses > 100):
    return buildOkResponse("[]")  

  if (ctr_responses % 10 == 2):
    return  # Return nothing

  if (ctr_responses % 10 == 3):
    return buildOkResponse("") # Return empty message

  if (ctr_responses % 10 == 4):
    return buildOkResponse(getEventHead(nodeName)) # Return part of a json event

  if (ctr_responses % 10 == 5):
    return buildEmptyResponse(404) # Return empty message with status code

  if (ctr_responses % 10 == 6):
    sleep(60)


  msg = getEventHead(nodeName)

  for i in range(100):
    seqNr = i+(ctr_responses-1)
    if i != 0: msg = msg + ","
    fileName = createFileName(nodeName, seqNr, "1MB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    fileMap[seqNr] = seqNr

  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc121(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 100):
    return buildOkResponse("[]")

  nodeName = createNodeName(0)
  msg = getEventHead(nodeName)

  fileName = ""
  for i in range(100):
    seqNr = i+(ctr_responses-1)
    if (seqNr%10 == 0):     # Every 10th file is "missing"
      fileName = createMissingFileName(nodeName, seqNr, "1MB")
    else:
      fileName = createFileName(nodeName, seqNr, "1MB")
      fileMap[seqNr] = seqNr

    if i != 0: msg = msg + ","
    msg = msg + getEventName(fileName,ftptype,"onap","pano")

  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc122(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 100):
    return buildOkResponse("[]")  

  nodeName = createNodeName(0)
  msg = getEventHead(nodeName)

  for i in range(100):
    fileName = createFileName(nodeName, 0, "1MB")  # All files identical names
    if i != 0: msg = msg + ","
    msg = msg + getEventName(fileName,ftptype,"onap","pano")

  fileMap[0] = 0
  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")


def tc1000(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  nodeName = createNodeName(0)
  msg = getEventHead(nodeName)

  for i in range(100):
    seqNr = i+(ctr_responses-1)
    if i != 0: msg = msg + ","
    fileName = createFileName(nodeName, seqNr, "1MB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    fileMap[seqNr] = seqNr

  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc1001(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  nodeName = createNodeName(0)
  msg = getEventHead(nodeName)

  for i in range(100):
    seqNr = i+(ctr_responses-1)
    if i != 0: msg = msg + ","
    fileName = createFileName(nodeName, seqNr, "5MB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    fileMap[seqNr] = seqNr

  msg = msg + getEventEnd()
  ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc510(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 5):
    return buildOkResponse("[]")  

  msg = ""

  for pnfs in range(700):  # build events for 700 MEs
    if (pnfs > 0):
      msg = msg + ","
    nodeName = createNodeName(pnfs)
    msg = msg + getEventHead(nodeName)
    seqNr = (ctr_responses-1)
    fileName = createFileName(nodeName, seqNr, "1MB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    seqNr = seqNr + pnfs*1000000 #Create unique id for this node and file
    fileMap[seqNr] = seqNr
    msg = msg + getEventEnd()
    ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc511(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1

  if (ctr_responses > 5):
    return buildOkResponse("[]")  

  msg = ""

  for pnfs in range(700):  # build events for 700 MEs
    if (pnfs > 0):
      msg = msg + ","
    nodeName = createNodeName(pnfs)
    msg = msg + getEventHead(nodeName)
    seqNr = (ctr_responses-1)
    fileName = createFileName(nodeName, seqNr, "1KB")
    msg = msg + getEventName(fileName,ftptype,"onap","pano")
    seqNr = seqNr + pnfs*1000000 #Create unique id for this node and file
    fileMap[seqNr] = seqNr
    msg = msg + getEventEnd()
    ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")

def tc710(ftptype):
  global ctr_responses
  global ctr_unique_files
  global ctr_events

  ctr_responses = ctr_responses + 1
  
  if (ctr_responses > 100):
    return buildOkResponse("[]")

  msg = ""
  
  batch = (ctr_responses-1)%20;  

  for pnfs in range(35):  # build events for 35 PNFs at a time. 20 batches -> 700
    if (pnfs > 0):
      msg = msg + ","
    nodeName = createNodeName(pnfs + batch*35)
    msg = msg + getEventHead(nodeName)

    for i in range(100):  # 100 files per event
      seqNr = i + int((ctr_responses-1)/20);
      if i != 0: msg = msg + ","
      fileName = createFileName(nodeName, seqNr, "1MB")
      msg = msg + getEventName(fileName,ftptype,"onap","pano")
      seqNr = seqNr + (pnfs+batch*35)*1000000 #Create unique id for this node and file
      fileMap[seqNr] = seqNr

    msg = msg + getEventEnd()
    ctr_events = ctr_events+1

  return buildOkResponse("["+msg+"]")


#Mapping FTPS TCs
def tc200(ftptype):
  return tc100(ftptype)
def tc201(ftptype):
  return tc101(ftptype)
def tc202(ftptype):
  return tc102(ftptype)

def tc210(ftptype):
  return tc110(ftptype)
def tc211(ftptype):
  return tc111(ftptype)
def tc212(ftptype):
  return tc112(ftptype)
def tc213(ftptype):
  return tc113(ftptype)

def tc220(ftptype):
  return tc120(ftptype)
def tc221(ftptype):
  return tc121(ftptype)
def tc222(ftptype):
  return tc122(ftptype)
  
def tc610(ftptype):
  return tc510(ftptype)
def tc611(ftptype):
  return tc511(ftptype)
  
def tc810(ftptype):
  return tc710(ftptype)

def tc2000(ftptype):
  return tc1000(ftptype)
def tc2001(ftptype):
  return tc1001(ftptype)

#### Functions to build json messages and respones ####

def createNodeName(index):
    return "PNF"+str(index);

def createFileName(nodeName, index, size):
    return "A20000626.2315+0200-2330+0200_" + nodeName + "-" + str(index) + "-" +size + ".tar.gz";

def createMissingFileName(nodeName, index, size):
    return "AMissingFile_" + nodeName + "-" + str(index) + "-" +size + ".tar.gz";


# Function to build fixed beginning of an event

def getEventHead(nodename):
  global pnfMap
  pnfMap.add(nodename) 
  headStr = """
        {
          "event": {
            "commonEventHeader": {
              "startEpochMicrosec": 8745745764578,
              "eventId": "FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1",
              "timeZoneOffset": "UTC+05.30",
              "internalHeaderFields": {
                "collectorTimeStamp": "Tue, 09 18 2018 10:56:52 UTC"
              },
              "priority": "Normal",
              "version": "4.0.1",
              "reportingEntityName": \"""" + nodename + """",
              "sequence": 0,
              "domain": "notification",
              "lastEpochMicrosec": 8745745764578,
              "eventName": "Noti_RnNode-Ericsson_FileReady",
              "vesEventListenerVersion": "7.0.1",
              "sourceName": \"""" + nodename + """"
            },
            "notificationFields": {
              "notificationFieldsVersion": "2.0",
              "changeType": "FileReady",
              "changeIdentifier": "PM_MEAS_FILES",
              "arrayOfNamedHashMap": [
          """ 
  return headStr

# Function to build the variable part of an event
def getEventName(fn,type,user,passwd):
    port = SFTP_PORT
    ip = sftp_ip
    if (type == "ftps"):
        port = FTPS_PORT
        ip = ftps_ip
        
    nameStr =        """{
                  "name": \"""" + fn + """",
                  "hashMap": {
                    "fileFormatType": "org.3GPP.32.435#measCollec",
                    "location": \"""" + type + """://""" + user + """:""" + passwd + """@""" + ip + """:""" + str(port) + """/""" + fn + """",
                    "fileFormatVersion": "V10",
                    "compression": "gzip"
                  }
                } """
    return nameStr

# Function to build fixed end of an event
def getEventEnd():
    endStr =  """
              ]
            }
          }
        }
        """
    return endStr

# Function to build an OK reponse from a message string
def buildOkResponse(msg):
  response = app.response_class(
      response=str.encode(msg),
      status=200,
      mimetype='application/json')
  return response

# Function to build an empty message with status
def buildEmptyResponse(status_code):
  response = app.response_class(
      response=str.encode(""),
      status=status_code,
      mimetype='application/json')
  return response


if __name__ == "__main__":

    # IP addresses to use for ftp servers, using localhost if not env var is set
    sftp_ip = os.environ.get('SFTP_SIM_IP', 'localhost')
    ftps_ip = os.environ.get('FTPS_SIM_IP', 'localhost')
    
    

    #Counters
    ctr_responses = 0
    ctr_requests = 0
    ctr_unique_files = 0
    ctr_events = 0
    startTime = time.time()

    #Keeps all responded file names
    fileMap = {}

    #Keeps all responded PNF names
    pnfMap = set()

    tc_num = "Not set"
    tc_help = "Not set"

    parser = argparse.ArgumentParser()

#SFTP TCs with single ME 
    parser.add_argument(
        '--tc100',
        action='store_true',
        help='TC100 - One ME, SFTP, 1 1MB file, 1 event')
    parser.add_argument(
        '--tc101',
        action='store_true',
        help='TC101 - One ME, SFTP, 1 5MB file, 1 event')
    parser.add_argument(
        '--tc102',
        action='store_true',
        help='TC102 - One ME, SFTP, 1 50MB file, 1 event')

    parser.add_argument(
        '--tc110',
        action='store_true',
        help='TC110 - One ME, SFTP, 1MB files, 1 file per event, 100 events, 1 event per poll.')
    parser.add_argument(
        '--tc111',
        action='store_true',
        help='TC111 - One ME, SFTP, 1MB files, 100 files per event, 100 events, 1 event per poll.')
    parser.add_argument(
        '--tc112',
        action='store_true',
        help='TC112 - One ME, SFTP, 5MB files, 100 files per event, 100 events, 1 event per poll.')
    parser.add_argument(
        '--tc113',
        action='store_true',
        help='TC113 - One ME, SFTP, 1MB files, 100 files per event, 100 events. All events in one poll.')

    parser.add_argument(
        '--tc120',
        action='store_true',
        help='TC120 - One ME, SFTP, 1MB files, 100 files per event, 100 events, 1 event per poll. 10% of replies each: no response, empty message, slow response, 404-error, malformed json')
    parser.add_argument(
        '--tc121',
        action='store_true',
        help='TC121 - One ME, SFTP, 1MB files, 100 files per event, 100 events, 1 event per poll. 10% missing files')
    parser.add_argument(
        '--tc122',
        action='store_true',
        help='TC122 - One ME, SFTP, 1MB files, 100 files per event, 100 events. 1 event per poll. All files with identical name. ')

    parser.add_argument(
        '--tc1000',
        action='store_true',
        help='TC1000 - One ME, SFTP, 1MB files, 100 files per event, endless number of events, 1 event per poll')
    parser.add_argument(
        '--tc1001',
        action='store_true',
        help='TC1001 - One ME, SFTP, 5MB files, 100 files per event, endless number of events, 1 event per poll')

# SFTP TCs with multiple MEs
    parser.add_argument(
        '--tc510',
        action='store_true',
        help='TC510 - 700 MEs, SFTP, 1MB files, 1 file per event, 3500 events, 700 event per poll.')
    
    parser.add_argument(
        '--tc511',
        action='store_true',
        help='TC511 - 700 MEs, SFTP, 1KB files, 1 file per event, 3500 events, 700 event per poll.')

    parser.add_argument(
        '--tc710',
        action='store_true',
        help='TC710 - 700 MEs, SFTP, 1MB files, 100 files per event, 3500 events, 35 event per poll.')

# FTPS TCs with single ME
    parser.add_argument(
        '--tc200',
        action='store_true',
        help='TC200 - One ME, FTPS, 1 1MB file, 1 event')
    parser.add_argument(
        '--tc201',
        action='store_true',
        help='TC201 - One ME, FTPS, 1 5MB file, 1 event')
    parser.add_argument(
        '--tc202',
        action='store_true',
        help='TC202 - One ME, FTPS, 1 50MB file, 1 event')

    parser.add_argument(
        '--tc210',
        action='store_true',
        help='TC210 - One ME, FTPS, 1MB files, 1 file per event, 100 events, 1 event per poll.')
    parser.add_argument(
        '--tc211',
        action='store_true',
        help='TC211 - One ME, FTPS, 1MB files, 100 files per event, 100 events, 1 event per poll.')
    parser.add_argument(
        '--tc212',
        action='store_true',
        help='TC212 - One ME, FTPS, 5MB files, 100 files per event, 100 events, 1 event per poll.')
    parser.add_argument(
        '--tc213',
        action='store_true',
        help='TC213 - One ME, FTPS, 1MB files, 100 files per event, 100 events. All events in one poll.')

    parser.add_argument(
        '--tc220',
        action='store_true',
        help='TC220 - One ME, FTPS, 1MB files, 100 files per event, 100 events, 1 event per poll. 10% of replies each: no response, empty message, slow response, 404-error, malformed json')
    parser.add_argument(
        '--tc221',
        action='store_true',
        help='TC221 - One ME, FTPS, 1MB files, 100 files per event, 100 events, 1 event per poll. 10% missing files')
    parser.add_argument(
        '--tc222',
        action='store_true',
        help='TC222 - One ME, FTPS, 1MB files, 100 files per event, 100 events. 1 event per poll. All files with identical name. ')

    parser.add_argument(
        '--tc2000',
        action='store_true',
        help='TC2000 - One ME, FTPS, 1MB files, 100 files per event, endless number of events, 1 event per poll')
    parser.add_argument(
        '--tc2001',
        action='store_true',
        help='TC2001 - One ME, FTPS, 5MB files, 100 files per event, endless number of events, 1 event per poll')    

    parser.add_argument(
        '--tc610',
        action='store_true',
        help='TC610 - 700 MEs, FTPS, 1MB files, 1 file per event, 3500 events, 700 event per poll.')

    parser.add_argument(
        '--tc611',
        action='store_true',
        help='TC611 - 700 MEs, FTPS, 1KB files, 1 file per event, 3500 events, 700 event per poll.')

    parser.add_argument(
        '--tc810',
        action='store_true',
        help='TC810 - 700 MEs, FTPS, 1MB files, 100 files per event, 3500 events, 35 event per poll.')

    args = parser.parse_args()



    if args.tc100:
        tc_num = "TC# 100"
    elif args.tc101:
        tc_num = "TC# 101"
    elif args.tc102:
        tc_num = "TC# 102"

    elif args.tc110:
        tc_num = "TC# 110"
    elif args.tc111:
        tc_num = "TC# 111"
    elif args.tc112:
        tc_num = "TC# 112"
    elif args.tc113:
        tc_num = "TC# 113"

    elif args.tc120:
        tc_num = "TC# 120"
    elif args.tc121:
        tc_num = "TC# 121"
    elif args.tc122:
        tc_num = "TC# 122"

    elif args.tc1000:
        tc_num = "TC# 1000"
    elif args.tc1001:
        tc_num = "TC# 1001"

    elif args.tc510:
        tc_num = "TC# 510"
    elif args.tc511:
        tc_num = "TC# 511"
        
    elif args.tc710:
        tc_num = "TC# 710"

    elif args.tc200:
        tc_num = "TC# 200"
    elif args.tc201:
        tc_num = "TC# 201"
    elif args.tc202:
        tc_num = "TC# 202"

    elif args.tc210:
        tc_num = "TC# 210"
    elif args.tc211:
        tc_num = "TC# 211"
    elif args.tc212:
        tc_num = "TC# 212"
    elif args.tc213:
        tc_num = "TC# 213"

    elif args.tc220:
        tc_num = "TC# 220"
    elif args.tc221:
        tc_num = "TC# 221"
    elif args.tc222:
        tc_num = "TC# 222"

    elif args.tc2000:
        tc_num = "TC# 2000"
    elif args.tc2001:
        tc_num = "TC# 2001"


    elif args.tc610:
        tc_num = "TC# 610"
    elif args.tc611:
        tc_num = "TC# 611"
           
    elif args.tc810:
        tc_num = "TC# 810"

    else:
        print("No TC was defined")
        print("use --help for usage info")
        sys.exit()

    print("TC num: " + tc_num)
    
        
    print("Using " + sftp_ip + " for sftp server address in file urls.")
    print("Using " + ftps_ip + " for ftps server address in file urls.")

    app.run(port=HOST_PORT, host=HOST_IP)
