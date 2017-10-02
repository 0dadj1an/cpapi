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
    custcomm_data = payload
    response = api_call(ipaddress, 443, command, custcomm_data, sid)
    try:
        response = json.dumps(response, sort_keys=True, indent=4)
        return(response)
    except TypeError:
        return(response)
