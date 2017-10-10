import json, requests
from app import app

requests.packages.urllib3.disable_warnings()

def api_call(ipaddress, port, command, json_payload, sid):
    '''The backbone of all calls issued to Check Point API.'''
    url = 'https://' + str(ipaddress) + ':' + str(port) + '/web_api/' + command
    if sid == None:
        request_headers = {'Content-Type' : 'application/json', 'User-Agent': 'CPAPI v0.4.3'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'User-Agent': 'CPAPI v0.4.3', 'X-chkp-sid' : sid}
    try:
        response = requests.post(url, data=json.dumps(json_payload), headers=request_headers, timeout=(30, 300), verify=False)
        return(response)
    except requests.exceptions.RequestException as e:
        app.logger.error('{}'.format(e))
        return ('Error: {}'.format(e))
