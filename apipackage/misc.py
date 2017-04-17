#Import Post
from apipackage.post import api_call

#Method to retrieve gateways-and-servers
def getalltargets(usrdef_sship, sid):
    get_targets_data = {'offset':0}
    get_targets_result = api_call(usrdef_sship, 443, 'show-gateways-and-servers', get_targets_data ,sid)
    targetslist = []
    for obj in get_targets_result["objects"]:
        targetslist.append(obj["name"])
    return (targetslist)

#Method to run script
def runcommand(usrdef_sship, target, name, command, sid):
    run_script_data = {'script-name':name, 'script':command, 'targets':target}
    get_targets_result = api_call(usrdef_sship, 443, 'run-script', run_script_data , sid)

#Method to put file
def putfile(usrdef_sship, target, path, name, contents, sid):
    put_file_data = {'file-path':path, 'file-name':name, 'file-content':contents, 'targets':target}
    put_file_result = api_call(usrdef_sship, 443, 'put-file', put_file_data , sid)
