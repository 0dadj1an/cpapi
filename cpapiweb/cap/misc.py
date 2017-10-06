from cap.post import api_call
from cap.utility import base64_ascii
import ast, json, time

def customcommand(ipaddress, command, payload, sid):
    try:
        payload = ast.literal_eval(payload)
    except ValueError:
        response = 'Invalid input provided.'
        return(response)
    except Exception as exc:
        response = exc
        return(exc)
    response = api_call(ipaddress, 443, command, payload, sid)
    return(response)

def getalltargets(ipaddress, sid):
    get_targets_data = {'limit':500}
    get_targets_result = api_call(ipaddress, 443, 'show-gateways-and-servers', get_targets_data ,sid)
    alltargets = []
    for obj in get_targets_result.json()["objects"]:
        alltargets.append(obj["name"])
    return(alltargets)

def runcommand(ipaddress, target, scriptcontent, sid):
    taskreturn = []
    run_script_data = {'script-name':'cpapi', 'script':scriptcontent, 'targets':target}
    response = api_call(ipaddress, 443, 'run-script', run_script_data , sid)
    if response.status_code == 200:
        if 'tasks' in response.json():
            for task in response.json()['tasks']:
                tasktrg = task['target']
                taskid = task['task-id']
                taskperc = 0
                while taskperc < 100:
                    taskresponse = gettask(ipaddress, taskid, sid)
                    taskperc = taskresponse.json()['tasks'][0]['progress-percentage']
                    if taskperc == 100:
                        if taskresponse.json()['tasks'][0]['task-details'][0]['responseMessage']:
                            base64resp = taskresponse.json()['tasks'][0]['task-details'][0]['responseMessage']
                            asciiresp = base64_ascii(base64resp)
                            taskreturn.append({'target':tasktrg, 'status':taskresponse.json()['tasks'][0]['status'],
                                               'response':asciiresp})
                        taskreturn.append({'target':tasktrg, 'status':taskresponse.json()['tasks'][0]['status'],
                                           'response':'Not Available'})
                    time.sleep(1)
            return(taskreturn)
    elif response.status_code == 404:
        return(response.text)
    else:
        return(response)

def gettask(ipaddress, task, sid):
    get_task_data = {'task-id':task, 'details-level':'full'}
    response = api_call(ipaddress, 443, 'show-task', get_task_data, sid)
    return(response)

def getallcommands(ipaddress, sid):
    commandlist = []
    getcommands_data = {}
    getcommands_result = api_call(ipaddress, 443, 'show-commands', getcommands_data, sid)
    for obj in getcommands_result.json()['commands']:
        commandlist.append(obj['name'])
    return(commandlist)
