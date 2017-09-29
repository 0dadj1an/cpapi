import json, requests
from datetime import datetime

filename = "logfile.txt"
try:
    with open(filename) as file:
        pass
except IOError:
    logfile = open((filename), "w+")

def api_call(ipaddress, port, command, json_payload, sid):
    url = 'https://' + str(ipaddress) + ':' + str(port) + '/web_api/' + command
    if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url, data=json.dumps(json_payload), headers=request_headers, timeout=(30, 300), verify=False)
        if r.status_code == 200:
            thetime = str(datetime.now())
            if command == 'login':
                json_payload['password'] = '*****'
            logfile = open((filename), "a")
            logfile.write("Time: {}\nCommand: {}".format(thetime, command) + "\n")
            logfile.write("Payload: {}".format(json_payload) + "\n")
            logfile.write("Response:\n" + json.dumps(r.json(), sort_keys=True, indent=4) + "\n")
            logfile.close()
            return (r.json())
        else:
            thetime = str(datetime.now())
            if command == 'login':
                json_payload['password'] = '*****'
            logfile = open((filename), "a")
            logfile.write("Time: {}\nCommand: {}".format(thetime, command) + "\n")
            logfile.write("Payload: {}".format(json_payload) + "\n")
            logfile.write("Response:\n" + json.dumps(r.json(), sort_keys=True, indent=4) + "\n")
            logfile.close()
            return (r.json())
    except:
        logfile = open((filename), "a")
        logfile.write("Exception Occured")
        logfile.close()
