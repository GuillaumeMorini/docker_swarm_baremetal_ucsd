#!/usr/bin/env python2
import httplib2
import urllib
import json
import sys
import time
from datetime import datetime

protocol = "http"
host = "10.60.7.72"
key = {'X-Cloupia-Request-Key': 'AA7EC480A80744FA97DCF1B205E45817'}
timeout = 180
comment = sys.argv[1]

def UCSD_REST_API(opName,opData):
    http = httplib2.Http()
    url = protocol+'://'+host+'/app/api/rest?formatType=json&opName='+opName+'&opData='+urllib.quote_plus(opData)
    response, content = http.request(url, headers=key)
    if int(response['status']) != 200:
        print "Return code "+response['status']+" --> Error on operation "+opName+", with data: "+opData
        print "Full response: "+response
        print "Full content: "+content
        sys.exit(1)
    j = json.loads(content)
    return j

sr = sys.argv[1]

## Rollbacking this SR
result = UCSD_REST_API('userAPIRollbackWorkflow','{param0:"'+sr+'"}')
serviceRequest = str(result['serviceResult'])
print "Rollback of SR "+sr+" has been launched (with SR "+serviceRequest+"), please wait for completion..."

## Wait for completion
startTime = datetime.now()
while True:
    time.sleep(30)

    result = UCSD_REST_API('userAPIGetWorkflowStatus', '{param0:'+serviceRequest+'}')

    status = result['serviceResult']
    if status == 1:
        print "In Progress..."
    elif status == 3:
        print "Completed!"
        sys.exit()
    elif status == 2:
        print "Failed!!!"
        sys.exit(2)

    duration = datetime.now() - startTime
    if duration.total_seconds() > timeout:
        print "Timeout!"
        sys.exit(3)
