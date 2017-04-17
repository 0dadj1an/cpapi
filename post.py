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
    r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
    if r.status_code == None:
        messagebox.showinfo("Command Response", "No Response")
    elif r.status_code == 200:
        return (r.json())
    else:
        messagebox.showinfo("Command Response", r.json())
        return (r.json())
