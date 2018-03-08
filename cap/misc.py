import ast
import time

from cap.post import api_call
from cap.utility import base64_ascii


def pre_data(apisession):
    # Black omitted as defalut option.
    all_colors = [
        'aquamarine', 'blue', 'crete blue', 'burlywood', 'cyan',
        'dark green', 'khaki', 'orchid', 'dark orange', 'dark sea green', 'pink',
        'turquoise', 'dark blue', 'firebrick', 'brown', 'forest green', 'gold',
        'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon', 'coral',
        'sea green', 'sky blue', 'magenta', 'purple', 'slate blue', 'violet red',
        'navy blue', 'olive', 'orange', 'red', 'sienna', 'yellow'
    ]

    all_commands = getallcommands(apisession)
    all_targets = getalltargets(apisession)
    all_layers = getalllayers(apisession)
    return {
        'all_colors': all_colors,
        'all_commands': all_commands,
        'all_targets': all_targets,
        'all_layers': all_layers}

def getalllayers(apisession):
    """Retrieve all rule base layers from management server."""
    get_layers_result = api_call(apisession.ipaddress, 443,
                                 'show-access-layers', {}, apisession.sid)
    return [(layer['name'], layer['uid'])
            for layer in get_layers_result.json()['access-layers']]


def customcommand(apisession, command, payload):
    """Validate payload and send command to server."""
    try:
        payload = ast.literal_eval(payload)
    except ValueError:
        response = 'Invalid input provided.'
        return response
    except Exception as exc:
        response = exc
        return exc
    response = api_call(apisession.ipaddress, 443, command, payload,
                        apisession.sid)
    return response


def getallcommands(apisession):
    """Get all available commands for custom command page."""
    getcommands_result = api_call(apisession.ipaddress, 443, 'show-commands',
                                  {}, apisession.sid)
    return [obj['name'] for obj in getcommands_result.json()['commands']]


def getalltargets(apisession):
    """Get all gateways and servers from Check Point."""
    get_targets_data = {'limit': 500}
    get_targets_result = api_call(apisession.ipaddress, 443,
                                  'show-gateways-and-servers',
                                  get_targets_data, apisession.sid)
    return [obj['name'] for obj in get_targets_result.json()['objects']]


def runcommand(apisession, target, scriptcontent):
    """Issue command against Check Point targets, verify task is complete on each gateways
    and return response for each target."""
    taskreturn = []
    run_script_data = {
        'script-name': 'cpapi',
        'script': scriptcontent,
        'targets': target
    }
    response = api_call(apisession.ipaddress, 443, 'run-script',
                        run_script_data, apisession.sid)
    if response.status_code == 200:
        if 'tasks' in response.json():
            for task in response.json()['tasks']:
                tasktrg = task['target']
                taskid = task['task-id']
                taskperc = 0
                while taskperc < 100:
                    taskresponse = gettask(apisession, taskid)
                    taskperc = taskresponse.json()['tasks'][0][
                        'progress-percentage']
                    if taskperc == 100:
                        if taskresponse.json()['tasks'][0]['task-details'][0][
                                'responseMessage']:
                            base64resp = taskresponse.json()['tasks'][0][
                                'task-details'][0]['responseMessage']
                            asciiresp = base64_ascii(base64resp)
                            taskreturn.append({
                                'target':
                                tasktrg,
                                'status':
                                taskresponse.json()['tasks'][0]['status'],
                                'response':
                                asciiresp
                            })
                        else:
                            taskreturn.append({
                                'target':
                                tasktrg,
                                'status':
                                taskresponse.json()['tasks'][0]['status'],
                                'response':
                                'Not Available'
                            })
                    time.sleep(1)
            return taskreturn
    elif response.status_code == 404:
        return response.text
    else:
        return response


def gettask(apisession, task):
    """Function for runcommand to get task status."""
    get_task_data = {'task-id': task, 'details-level': 'full'}
    response = api_call(apisession.ipaddress, 443, 'show-task', get_task_data,
                        apisession.sid)
    return response
