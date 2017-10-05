from cap.post import api_call
import ast, json

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
    run_script_data = {'script-name':'cpapi', 'script':scriptcontent, 'targets':target}
    response = api_call(ipaddress, 443, 'run-script', run_script_data , sid)
