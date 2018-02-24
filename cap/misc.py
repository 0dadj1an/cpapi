import ast
import time

from cap.post import api_call


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
