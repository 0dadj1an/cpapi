#Import
import json, requests
from tkinter import messagebox

#Method to carry webapi call
def api_call(ip_addr, port, command, json_payload, sid):
    #Form URL with variables
    url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
    #If for first call which will have no session ID
    if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    #Payload with session id
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    #Try to send post to API, disable ssl warning to prevent some cases of crashing
    #when writing to stdin, stout, sterr
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, timeout=(30, 90), verify=False)
        if r.status_code == 200:
            return (r.json())
        #On API Error message give feedback
        else:
            messagebox.showinfo("Command Response", r.json())
            return (r.json())
    #Catch some request exceptions
    except requests.exceptions.Timeout:
        messagebox.showinfo("Command Response", "Request Timeout")
    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Command Response", "Connection Error")
    except:
        messagebox.showinfo("Command Response", "Uh oh...")
