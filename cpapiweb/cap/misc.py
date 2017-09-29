from cap.post import api_call

def customcommand(ipaddress, command, payload, sid):
    payload = eval(payload)
    custcomm_data = payload
    response = api_call(ipaddress, 443, command, custcomm_data, sid)
    return(response)
