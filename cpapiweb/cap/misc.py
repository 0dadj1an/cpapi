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
