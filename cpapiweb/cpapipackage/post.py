#Import
import json, requests
from tkinter import messagebox
from datetime import datetime

# Check for log file, create if it does not exist
filename = "logfile.txt"
try:
    with open(filename) as file:
        pass
except IOError:
    logfile = open((filename), "w+")

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
        r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, timeout=(30, 300), verify=False)
        if r.status_code == 200:
            #logwrite(command, json_payload)
            thetime = str(datetime.now())
            if command == 'login':
                json_payload['password'] = '*****'
            logfile = open((filename), "a")
            logfile.write("Time: {}\nCommand: {}".format(thetime, command) + "\n")
            logfile.write("Payload: {}".format(json_payload) + "\n")
            logfile.write("Response:\n" + json.dumps(r.json(), sort_keys=True, indent=4) + "\n")
            logfile.close()
            return (r.json())
        #On API Error message give feedback
        else:
            #logwrite(command, json_payload)
            thetime = str(datetime.now())
            if command == 'login':
                json_payload['password'] = '*****'
            logfile = open((filename), "a")
            logfile.write("Time: {}\nCommand: {}".format(thetime, command) + "\n")
            logfile.write("Payload: {}".format(json_payload) + "\n")
            logfile.write("Response:\n" + json.dumps(r.json(), sort_keys=True, indent=4) + "\n")
            logfile.close()
            messagebox.showinfo("Command Response", r.json())
            return (r.json())
    #Catch some request exceptions
    except requests.exceptions.Timeout:
        messagebox.showinfo("Command Response", "Request Timeout")
    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Command Response", "Connection Error")
    except:
        messagebox.showinfo("Command Response", "Uh oh...")
