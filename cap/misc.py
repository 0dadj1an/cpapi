import ast
import time

from cap.post import api_call
from cap.utility import base64_ascii


def pre_data(apisession):
    # Black omitted as defalut option.
    apisession.all_colors = [
        'aquamarine', 'blue', 'crete blue', 'burlywood', 'cyan',
        'dark green', 'khaki', 'orchid', 'dark orange', 'dark sea green', 'pink',
        'turquoise', 'dark blue', 'firebrick', 'brown', 'forest green', 'gold',
        'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon', 'coral',
        'sea green', 'sky blue', 'magenta', 'purple', 'slate blue', 'violet red',
        'navy blue', 'olive', 'orange', 'red', 'sienna', 'yellow'
    ]
    apisession.all_commands = getallcommands(apisession)
    apisession.all_targets = getalltargets(apisession)
    apisession.all_layers = getalllayers(apisession)


def getalllayers(apisession):
    """Retrieve all rule base layers from management server."""
    all_layers = []
    apisession.offset = 0
    get_layers_data = {'limit': apisession.limit, 'offset': apisession.offset}
    get_layers_result = api_call(apisession.ipaddress, 443, 'show-access-layers', get_layers_data, apisession.sid)
    for layer in get_layers_result.json()['access-layers']:
        all_layers.append((layer['name'], layer['uid']))

    while get_layers_result.json()['to'] != get_layers_result.json()['total']:
        apisession.offset += 50
        get_more_layers = {'limit': apisession.limit, 'offset': apisession.offset}
        get_layers_result = api_call(apisession.ipaddress, 443, 'show-access-layers', get_more_layers, apisession.sid)
        for layer in get_layers_result.json()['access-layers']:
            all_layers.append((layer['name'], layer['uid']))

    return all_layers


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
    all_targets = []
    apisession.offset = 0
    get_targets_data = {'limit': apisession.limit, 'offset': apisession.offset}
    get_targets_result = api_call(apisession.ipaddress, 443, 'show-gateways-and-servers', get_targets_data, apisession.sid)
    for target in get_targets_result.json()['objects']:
        all_targets.append(target['name'])

    while get_targets_result.json()['to'] != get_targets_result.json()['total']:
        apisession.offset += 50
        get_more_targets = {'limit': apisession.limit, 'offset': apisession.offset}
        get_targets_result = api_call(apisession.ipaddress, 443, 'show-gateways-and-servers', get_more_targets, apisession.sid)
        for target in get_targets_result.json()['objects']:
            all_targets.append(target['name'])

    return all_targets


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
