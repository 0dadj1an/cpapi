class misc:

    #Method to retrieve gateways-and-servers
    def getalltargets(usrdef_sship, sid):
        #Retrieve Targets
        get_targets_data = {'offset':0}
        get_targets_result = ac(usrdef_sship, 443, 'show-gateways-and-servers', get_targets_data ,sid)
        return (get_targets_result)

    #Method to run script
    def runscript(usrdef_sship, target, name, command, sid):
        run_script_data = {'script-name':name, 'script':command, 'targets':target}
        get_targets_result = ac(usrdef_sship, 443, 'run-script', run_script_data , sid)

    #Method to put file
    def putfile(usrdef_sship, target, path, name, contents, sid):
        put_file_data = {'file-path':path, 'file-name':name, 'file-content':contents, 'targets':target}
        put_file_result = ac(usrdef_sship, 443, 'put-file', put_file_data , sid)
