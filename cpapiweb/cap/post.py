import json, requests

def api_call(ipaddress, port, command, json_payload, sid):
    url = 'https://' + str(ipaddress) + ':' + str(port) + '/web_api/' + command
    if sid == None:
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.post(url, data=json.dumps(json_payload), headers=request_headers, timeout=(30, 300), verify=False)
        if response.status_code == 403:
            return(response)
        else:
            return(response.json())
    except requests.exceptions.RequestException as e:
        return ('Error: {}'.format(e))
