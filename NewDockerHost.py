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
timeout = 360
#workflowName = "Add Docker host"
#workflowInputs = '{"name":"Hostname","value":"'+sys.argv[1]+'"}'
workflowName = "Add host to Docker Swarm"
workflowInputs = ''

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

## Execute a workflow
#result = UCSD_REST_API('userAPISubmitWorkflowServiceRequest', '{param0:"'+workflowName+'",param1:{"list":['+workflowInputs+']},param2:-1}')
result = UCSD_REST_API('userAPISubmitWorkflowServiceRequest', '{param0:"'+workflowName+'",param1:{}, param2:-1}')
serviceRequest = str(result['serviceResult'])
print "SR "+serviceRequest+" has been created for workflow "+workflowName+", please wait for completion..."

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
