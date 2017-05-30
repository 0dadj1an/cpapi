#Import
import json, requests
from tkinter import messagebox

#Method to carry webapi call
def api_call(ip_addr, port, command, json_payload, sid):
    url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
    if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, timeout=(30, 90), verify=False)
        if r.status_code == 200:
            return (r.json())
        else:
            messagebox.showinfo("Command Response", r.json())
            return (r.json())
    except requests.exceptions.Timeout:
        messagebox.showinfo("Command Response", "Request Timeout")
    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Command Response", "Connection Error")
