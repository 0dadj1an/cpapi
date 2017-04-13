#Import Things
import sys, time, json
#Import Requests
import requests
#Import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#Global Variables
sid = "tbd"
usrdef_sship = "tbd"

#Class for main frame
class apiapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Check Point API Tool")
        self.iconbitmap("cpapiicon.ico")
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, AddHost, AddNetwork, AddGroup, ObjectToGroup, ImportHosts,
            ExportHosts, ImportNetworks, ExportNetworks, ImportGroups, ExportGroups,
            ImportRules, ExportRules, RunScript, dthomas):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nesw")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

#Class for starting window
class StartPage(tk.Frame):

    #Method to carry webapi call
    def api_call(self, ip_addr, port, command, json_payload, sid):
        url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
        if sid == '':
            request_headers = {'Content-Type' : 'application/json'}
        else:
            request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
        r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
        return (r.json())

    #Method to login over api
    def login(self, ip, usrdef_username, usrdef_pass):
        payload = {'user':usrdef_username, 'password' : usrdef_pass}
        response = self.api_call(ip, 443, 'login', payload, '')
        global usrdef_sship
        usrdef_sship = ip
        global sid
        #Return Error Message if sid does not exist
        if 'sid' not in response:
            messagebox.showinfo("Login Response", response["message"])
        elif 'sid' in response:
            messagebox.showinfo("Login Response", "Login Successful")
            sid = (response["sid"])
        ### CURRENTLY NOT WORKING ###
        else:
            messagebox.showinfo("Login Response", "Connection Failed")

    #Method to publish api session
    def publish(self):
        publish_result = self.api_call(usrdef_sship, 443, 'publish', {} ,sid)
        #Return Successful if task-id exist
        if 'task-id' in publish_result:
            messagebox.showinfo("Publish Response", "Publish Successful")
        else:
            messagebox.showinfo("Publish Response", "Publish Failed")

    #Method to logout over api
    def logout(self):
        logout_result = self.api_call(usrdef_sship, 443,"logout", {},sid)
        messagebox.showinfo("Logout Response", logout_result)


    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        label = ttk.Label(self, text="Credentials for Session")
        label.configure(background="#494949", foreground="#f44242")
        label.grid(row=0, columnspan=3)

        #Collect IP for connection
        sship_l = ttk.Label(self, text = "IP", background="#494949", foreground="#f44242")
        sship_l.grid(row=1, column=0, sticky=E)
        sship_e = Entry(self, bd=5)
        sship_e.grid(row=1, column=1)
        sship_e.configure(background="#ffffff")

        #Collect Username for connection
        username_l = ttk.Label(self, text = "Username", background="#494949", foreground="#f44242")
        username_l.grid(row=2, column=0, sticky=E)
        username_e = Entry(self, bd=5)
        username_e.grid(row=2, column=1)
        username_e.configure(background="#ffffff")

        #Collect Password for connection
        pass_l = ttk.Label(self, text = "Password",  background="#494949", foreground="#f44242")
        pass_l.grid(row=3, column=0, sticky=E)
        pass_e = Entry(self, bd=5, show="*")
        pass_e.grid(row=3, column=1)
        pass_e.configure(background="#ffffff")

        #Button to start session
        sessionb = ttk.Button(self, text="Connect", command=lambda: self.login(sship_e.get(), username_e.get(), pass_e.get()))
        sessionb.grid(row=1, column=2)

        #Button to publish session
        publishb = ttk.Button(self, text="Publish", command=lambda: self.publish())
        publishb.grid(row=2, column=2)

        #Button to logout session
        logoutb = ttk.Button(self, text="Logout", command=lambda: self.logout())
        logoutb.grid(row=3, column=2)

        #Create Space
        space_label = ttk.Label(self, background="#494949")
        space_label.grid(row=4)

        #Button to call add object to group
        addhosttogroup = ttk.Button(self, text="Add Object To Group", command=lambda: controller.show_frame("ObjectToGroup"))
        addhosttogroup.grid(row=5, column=3)

        #Button to call add host window
        addhostb = ttk.Button(self, text="Add Host", command=lambda: controller.show_frame("AddHost"))
        addhostb.grid(row=5)

        #Button to call add network window
        addnetworkb = ttk.Button(self, text="Add Network", command=lambda: controller.show_frame("AddNetwork"))
        addnetworkb.grid(row=5, column=1)

        #Button to call add group window
        addgroupb = ttk.Button(self, text="Add Group", command=lambda: controller.show_frame("AddGroup"))
        addgroupb.grid(row=5, column=2)

        #Button to call import hosts window
        imphostb = ttk.Button(self, text="Import Hosts", command=lambda: controller.show_frame("ImportHosts"))
        imphostb.grid(row=6, column=0)

        #Button to call export hosts window
        exphostsb = ttk.Button(self, text="Export Hosts", command=lambda: controller.show_frame("ExportHosts"))
        exphostsb.grid(row=7, column=0)

        #Button to call import networks window
        impnetsb = ttk.Button(self, text="Import Networks", command=lambda: controller.show_frame("ImportNetworks"))
        impnetsb.grid(row=6, column=1)

        #Button to call export networks window
        expnetsb = ttk.Button(self, text="Export Networks", command=lambda: controller.show_frame("ExportNetworks"))
        expnetsb.grid(row=7, column=1)

        #Button to call import groups window
        impnetsb = ttk.Button(self, text="Import Groups", command=lambda: controller.show_frame("ImportGroups"))
        impnetsb.grid(row=6, column=2)

        #Button to call export groups window
        expnetsb = ttk.Button(self, text="Export Groups", command=lambda: controller.show_frame("ExportGroups"))
        expnetsb.grid(row=7, column=2)

        #Button to call import rules window
        imprulesb = ttk.Button(self, text="Import Rules", command=lambda: controller.show_frame("ImportRules"))
        imprulesb.grid(row=6, column=3)

        #Button to call export rules window
        exprulesb = ttk.Button(self, text="Export Rules", command=lambda: controller.show_frame("ExportRules"))
        exprulesb.grid(row=7, column=3)

        #Create More Space
        more_space_label = ttk.Label(self, background="#494949")
        more_space_label.grid(row=8)

        #Button to call run-script window
        runscriptb = ttk.Button(self, text="Run Script", command=lambda: controller.show_frame("RunScript"))
        runscriptb.grid(row=9, column=0)

        #Butto to call dthomas window
        dthomb = ttk.Button(self, text="dthomas", command=lambda: controller.show_frame("dthomas"))
        dthomb.grid(row=9, column=1)

#Class for add host functionality
class AddHost(tk.Frame):

    #Method for adding a host object
    def addhost(self, hostname, hostip, hostcolor):
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
        new_host_result = StartPage.api_call(self, usrdef_sship, 443,'add-host', new_host_data ,sid)
        if 'creator' in new_host_result:
            messagebox.showinfo("Add Host Response", "Add Host Successful")
        else:
            messagebox.showinfo("Add Host Response", new_host_result)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Add Host")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Host Name
        hostname_l = ttk.Label(self, text = "Host Name", background="#494949", foreground="#f44242")
        hostname_l.grid(row=1, column=0, sticky=E)
        hostname_e = Entry(self, bd=5)
        hostname_e.grid(row=1, column=1)
        hostname_e.configure(background="#ffffff")

        #Host IP
        hostip_l = ttk.Label(self, text = "Host IP", background="#494949", foreground="#f44242")
        hostip_l.grid(row=2, column=0, sticky=E)
        hostip_e = Entry(self, bd=5)
        hostip_e.grid(row=2, column=1)
        hostip_e.configure(background="#ffffff")

        #Host Color
        hostcolor_l = ttk.Label(self, text="Host Color", background="#494949", foreground="#f44242")
        hostcolor_l.grid(row=3, column=0, sticky=E)
        defaultcolor = StringVar(self)
        defaultcolor.set("black")
        hostcolormenu = OptionMenu(self, defaultcolor, "black", "blue", "cyan", "gold", "green", "red", "orange", "yellow")
        hostcolormenu.grid(row=3, column=1)

        #Button to run command
        runapi = ttk.Button(self, text="Add Host", command=lambda: self.addhost(hostname_e.get(), hostip_e.get(), defaultcolor.get()))
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Class for add network functionality
class AddNetwork(tk.Frame):

    #Method for adding a network object
    def addnetwork(self, netname, netsub, netmask):
        new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask}
        new_network_result = StartPage.api_call(self, usrdef_sship, 443,'add-network', new_network_data ,sid)
        if 'creator' in new_network_result:
            messagebox.showinfo("Add Network Response", "Successful")
        else:
            messagebox.showinfo("Add Network Response", new_network_result)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Add Network")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Network Name
        netname_l = ttk.Label(self, text = "Network Name", background="#494949", foreground="#f44242")
        netname_l.grid(row=1, column=0, sticky=E)
        netname_e = Entry(self, bd=5)
        netname_e.grid(row=1, column=1)
        netname_e.configure(background="#ffffff")

        #Network Address
        netaddr_l = ttk.Label(self, text = "Mask-Length", background="#494949", foreground="#f44242")
        netaddr_l.grid(row=2, column=0, sticky=E)
        netaddr_e = Entry(self, bd=5)
        netaddr_e.grid(row=2, column=1)
        netaddr_e.configure(background="#ffffff")

        #Network Mask
        netmask_l = ttk.Label(self, text = "Subnet Mask", background="#494949", foreground="#f44242")
        netmask_l.grid(row=3, column=0, sticky=E)
        netmask_e = Entry(self, bd=5)
        netmask_e.grid(row=3, column=1)
        netmask_e.configure(background="#ffffff")

        #Button to run command
        runapi = ttk.Button(self, text="Add Network", command = lambda: self.addnetwork(netname_e.get(), netaddr_e.get(), netmask_e.get()))
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Class for add network functionality
class AddGroup(tk.Frame):

    #Method for adding a group object
    def addgroup(self, groupname):
        new_group_data = {'name':groupname}
        new_group_result = StartPage.api_call(self, usrdef_sship, 443,'add-group', new_group_data ,sid)
        if 'creator' in new_group_result:
            messagebox.showinfo("Add Group Response", "Successful")
        else:
            messagebox.showinfo("Add Group Response", new_group_result)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addgrouplabel = ttk.Label(self, text="Add Group")
        addgrouplabel.configure(background="#494949", foreground="#f44242")
        addgrouplabel.grid(row=0, column=0, columnspan=2)

        #Group Name
        groupname_l = ttk.Label(self, text = "Group Name", background="#494949", foreground="#f44242")
        groupname_l.grid(row=1, column=0, sticky=E)
        groupname_e = Entry(self, bd=5)
        groupname_e.grid(row=1, column=1)
        groupname_e.configure(background="#ffffff")

        #Button to run command
        runapi = ttk.Button(self, text="Add Group", command = lambda: self.addgroup(groupname_e.get()))
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Class for adding objects to a group functionality
class ObjectToGroup(tk.Frame):

    #Method to add host to group
    def addhostgroup(self, hostname, groupname):
        addhostgroup_data = {'name':hostname, 'groups':groupname}
        addhostgroup_result = StartPage.api_call(self, usrdef_sship, 443,'set-host', addhostgroup_data, sid)
        if 'creator' in addhostgroup_result:
            messagebox.showinfo("Add Host Response", "Successful")
        else:
            messagebox.showinfo("Add Host Response", addhostgroup_result)

    #Method to add network to group
    def addnetgroup(self, netname, groupname):
        addnetgroup_data = {'name':netname, 'groups':groupname}
        addnetgroup_result = StartPage.api_call(self, usrdef_sship, 443, 'set-network', addnetgroup_data, sid)
        if 'creator' in addnetgroup_result:
            messagebox.showinfo("Add Network Response", "Successful")
        else:
            messagebox.showinfo("Add Network Response", addnetgroup_result)

    #Method to add group to group
    def addgroupgroup(self, addgroupname, groupname):
        addgroup_data = {'name':addgroupname, 'groups':groupname}
        addgroupgroup_result = StartPage.api_call(self, usrdef_sship, 443, 'set-group', addgroup_data, sid)
        if 'creator' in addgroupgroup_result:
            messagebox.showinfo("Add Group Response", "Successful")
        else:
            messagebox.showinfo("Add Group Response", addgroupgroup_result)

    #Method to retrieve hosts,networks,groups
    def gethostnetgroup(self):
        #Create list for each type
        allhostlist = []
        allnetlist = []
        allgrouplist = []
        #API Call for each type
        show_hosts_data = {'offset':0, 'details-level':'standard'}
        show_hosts_result = StartPage.api_call(self, usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        show_groups_data = {'offset':0, 'details-level':'standard'}
        show_groups_result = StartPage.api_call(self, usrdef_sship, 443, 'show-groups', show_groups_data, sid)
        show_nets_data = {'offset':0, 'details-level':'standard'}
        show_nets_result = StartPage.api_call(self, usrdef_sship, 443, 'show-networks', show_nets_data, sid)
        #Parse out names only
        for host in show_hosts_result["objects"]:
            allhostlist.append(host["name"])
        for net in show_nets_result["objects"]:
            allnetlist.append(net["name"])
        for group in show_groups_result["objects"]:
            allgrouplist.append(group["name"])
        #Host Dropdown
        allhost = ttk.Label(self, text="All Hosts", background="#494949", foreground="#f44242")
        allhost.grid(row=2, column=0, sticky=E)
        defaulthost = StringVar(self)
        defaulthost.set("Select Host")
        hostmenu = OptionMenu(self, defaulthost, *allhostlist)
        hostmenu.grid(row=2, column=1)
        #Network Dropdown
        allnet = ttk.Label(self, text="All Networks", background="#494949", foreground="#f44242")
        allnet.grid(row=3, column=0, sticky=E)
        defaultnet = StringVar(self)
        defaultnet.set("Select Network")
        netmenu = OptionMenu(self, defaultnet, *allnetlist)
        netmenu.grid(row=3, column=1)
        #Group Dropdown
        allgroup1 = ttk.Label(self, text="All Groups", background="#494949", foreground="#f44242")
        allgroup1.grid(row=4, column=0, sticky=E)
        defaultaddgroup = StringVar(self)
        defaultaddgroup.set("Select Group")
        groupaddmenu = OptionMenu(self, defaultaddgroup, *allgrouplist)
        groupaddmenu.grid(row=4, column=1)
        #Target Group Dropdown
        allgroup2 = ttk.Label(self, text="All Groups", background="#494949", foreground="#f44242")
        allgroup2.grid(row=2, column=3)
        defaultgroup = StringVar(self)
        defaultgroup.set("Target Group")
        groupmenu = OptionMenu(self, defaultgroup, *allgrouplist)
        groupmenu.grid(row=3, column=3)

        #Button to add host to group
        hosttogroupb = ttk.Button(self, text="Add Host", command=lambda: self.addhostgroup(defaulthost.get(), defaultgroup.get()))
        hosttogroupb.grid(row=2, column=2)

        #Button to add network to group
        nettogroupb = ttk.Button(self, text="Add Network", command=lambda: self.addnetgroup(defaultnet.get(), defaultgroup.get()))
        nettogroupb.grid(row=3, column=2)

        #Button to add group to group
        grouptogroup = ttk.Button(self, text="Add Group", command=lambda: self.addgroupgroup(defaultaddgroup.get(), defaultgroup.get()))
        grouptogroup.grid(row=4, column=2)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Add Object to Group")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve objects
        runapi = ttk.Button(self, text="Get Objects", command=lambda: self.gethostnetgroup())
        runapi.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=2)

#Class for adding importhost functionality
class ImportHosts(tk.Frame):

    #Method for adding a host object for importhost
    def importaddhost(self, hostname, hostip, hostcolor, natset):
        natset = eval(natset)
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor, 'nat-settings':natset}
        new_host_result = StartPage.api_call(self, usrdef_sship, 443,'add-host', new_host_data ,sid)

    #Method to import host from csv file
    def importhosts(self, filename):
        csvhosts = open(filename, "r").read().split("\n")
        for line in csvhosts:
            apiprep = line.split(';')
            self.importaddhost(apiprep[0], apiprep[1], apiprep[2], apiprep[3])
        cvshosts.close()
        messagebox.showinfo("Import Host Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Import Hosts")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #File Selection
        file_l = ttk.Label(self, text = "CSV File Name", background="#494949", foreground="#f44242")
        file_l.grid(row=1, column=0, sticky=E)
        file_e = Entry(self, bd=5)
        file_e.grid(row=1, column=1)
        file_e.configure(background="#ffffff")

        #Button to import Hosts
        imphostb = ttk.Button(self, text="Import", command=lambda: self.importhosts(file_e.get()))
        imphostb.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=3)

        #Example file
        example_l = ttk.Label(self, text="Example file provided in repository!")
        example_l.configure(background="#494949", foreground="#f44242")
        example_l.grid(row=2, columnspan=2)

#Class for adding exporthost functionality
class ExportHosts(tk.Frame):

    #Method to export host to csv file
    def exporthosts(self):
        show_hosts_data = {'offset':0, 'details-level':'full'}
        show_hosts_result = StartPage.api_call(self, usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        hostexportfile = open(("exportedhosts.csv"), "w+")
        for host in show_hosts_result["objects"]:
            if 'nat-settings' in host:
                natsettings = host["nat-settings"]
                natsettings.pop('ipv6-address', None)
                natsettings = str(natsettings)
            hostexportfile = open(("exportedhosts.csv"), "a")
            hostexportfile.write(host["name"] + ";" + host["ipv4-address"] + ";" + host["color"] + ";")
            hostexportfile.write(natsettings)
            hostexportfile.write("\n")
        hostexportfile.close()
        messagebox.showinfo("Export Hosts Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Hosts")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to export hosts
        exphostb = ttk.Button(self, text="Export Hosts", command=lambda: self.exporthosts())
        exphostb.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)

#Class for adding importnetwork functionality
class ImportNetworks(tk.Frame):

    #Method for adding a network object for importnetworks
    def importaddnetwork(self, netname, netsub, netmask, netcolor, natset):
        natset = eval(natset)
        new_network_data = {'name':netname, 'subnet':netsub, 'mask-length':netmask, 'color':netcolor, 'nat-settings':natset}
        new_network_result = StartPage.api_call(self, usrdef_sship, 443,'add-network', new_network_data ,sid)

    #Method to import networks from csv
    def importnetworks(self, filename):
        csvnets = open(filename, "r").read().split("\n")
        for line in csvnets:
            apiprep = line.split(';')
            self.importaddnetwork(apiprep[0], apiprep[1], apiprep[2], apiprep[3], apiprep[4])
        csvnets.close()
        messagebox.showinfo("Import Network Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Import Networks")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #File Selection
        file_l = ttk.Label(self, text = "CSV File Name", background="#494949", foreground="#f44242")
        file_l.grid(row=1, column=0, sticky=E)
        file_e = Entry(self, bd=5)
        file_e.grid(row=1, column=1)
        file_e.configure(background="#ffffff")

        #Button to import networks
        exphostb = ttk.Button(self, text="Import Networks", command=lambda: self.importnetworks(file_e.get()))
        exphostb.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=3)

        #Example file
        example_l = ttk.Label(self, text="Example file provided in repository!")
        example_l.configure(background="#494949", foreground="#f44242")
        example_l.grid(row=2, columnspan=2)

#Class for adding exportnetwork functionality
class ExportNetworks(tk.Frame):

    #Method to export host to csv file
    def exportnetworks(self):
        show_networks_data = {'offset':0, 'details-level':'full'}
        show_networks_result = StartPage.api_call(self, usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
        networksexportfile = open(("exportednetworks.csv"), "w+")
        for network in show_networks_result["objects"]:
            networksexportfile = open(("exportednetworks.csv"), "a")
            if 'nat-settings' in network:
                natsettings = network["nat-settings"]
                natsettings.pop('ipv6-address', None)
                natsettings = str(natsettings)
            networksexportfile.write(network["name"] + ";" + str(network["subnet4"]) + ";" + str(network["mask-length4"]) + ";" + network["color"] + ";")
            networksexportfile.write(natsettings)
            networksexportfile.write("\n")
        networksexportfile.close()
        messagebox.showinfo("Export Network Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Networks")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to export networks
        exphostb = ttk.Button(self, text="Export Networks", command=lambda: self.exportnetworks())
        exphostb.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)

#Class for adding importgroup functionality
class ImportGroups(tk.Frame):

    #Method for adding a group object with members
    def addgroupmembers(self, groupname, members):
        new_group_data = {'name':groupname, 'members':members}
        new_group_result = StartPage.api_call(self, usrdef_sship, 443,'add-group', new_group_data ,sid)

    #Method to import group from csv
    def importgroups(self, filename):
        csvgroups = open(filename, "r").read().split()
        #Parse Exported Groups File
        for line in csvgroups:
            #Split Group name from members
            groupname = line.split(',')
            #Split Members from each other
            memberlist = groupname[1].split(';')
            #Pass to api, last element in memberlist is an empty string
            self.addgroupmembers(groupname[0], memberlist[0:-1])
        csvgroups.close()
        messagebox.showinfo("Import Groups Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Import Groups")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #File Selection
        file_l = ttk.Label(self, text = "CSV File Name", background="#494949", foreground="#f44242")
        file_l.grid(row=1, column=0, sticky=E)
        file_e = Entry(self, bd=5)
        file_e.grid(row=1, column=1)
        file_e.configure(background="#ffffff")

        #Button to import groups
        exphostb = ttk.Button(self, text="Import Groups", command=lambda: self.importgroups(file_e.get()))
        exphostb.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=3)

        #Example file
        example_l = ttk.Label(self, text="Example file provided in repository!")
        example_l.configure(background="#494949", foreground="#f44242")
        example_l.grid(row=2, columnspan=2)

#Class for adding exporthost functionality
class ExportGroups(tk.Frame):

    #Method to export host to csv file
    def exportgroups(self):
        show_groups_data = {'offset':0, 'details-level':'full'}
        show_groups_result = StartPage.api_call(self, usrdef_sship, 443, 'show-groups', show_groups_data ,sid)
        groupsexportfile = open(("exportedgroups.csv"), "w+")
        for group in show_groups_result["objects"]:
            groupsexportfile.write(group["name"] + ",")
            listofmembers = group["members"]
            for member in listofmembers:
                groupsexportfile.write(member["name"] + ";")
            groupsexportfile.write("\n")
        groupsexportfile.close()
        messagebox.showinfo("Export Groups Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Groups")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to export groups
        exphostb = ttk.Button(self, text="Export Groups", command=lambda: self.exportgroups())
        exphostb.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)

#Class for adding importrule functionality
class ImportRules(tk.Frame):

    #Method to add rule for importrules
    def importaddrules(self, num, name, src, dst, srv, act):
        add_rule_data = {'layer':'Network', 'position':num, 'name':name, 'source':src, 'destination':dst, 'service':srv, 'action':act}
        add_rule_result = StartPage.api_call(self, usrdef_sship, 443, 'add-access-rule', add_rule_data, sid)

    #Method to import rulebase from csv
    def importrules(self, filename):
        csvrules = open(filename, "r").read().split("\n")
        #Parse Exported Rules File
        for line in csvrules:
            #Split Rule Fields
            fullrule = line.split(',')
            print (fullrule)
            num = fullrule[0]
            name = fullrule[1]
            try:
                src = fullrule[2].split(';')
            except:
                src = fullrule[2]
            try:
                dst = fullrule[3].split(';')
            except:
                dst = fullrule[3]
            try:
                srv = fullrule[4].split(';')
            except:
                srv = fullrule[4]
            act = fullrule[5]
            self.importaddrules(num, name, src, dst, srv, act)
        csvrules.close()
        messagebox.showinfo("Import Rules Response", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Import Rulesbase")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #File Selection
        file_l = ttk.Label(self, text = "CSV File Name", background="#494949", foreground="#f44242")
        file_l.grid(row=1, column=0, sticky=E)
        file_e = Entry(self, bd=5)
        file_e.grid(row=1, column=1)
        file_e.configure(background="#ffffff")

        #Button to import networks
        exphostb = ttk.Button(self, text="Import Rulebase", command=lambda: self.importrules(file_e.get()))
        exphostb.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=3)

        #Example file
        example_l = ttk.Label(self, text="Example file provided in repository!")
        example_l.configure(background="#494949", foreground="#f44242")
        example_l.grid(row=2, columnspan=2)

#Class for adding exportrule functionality
class ExportRules(tk.Frame):

    #Method to retrieve available packages
    def getpackages(self):
        get_packages_data = {'offset':0, 'details-level':'full'}
        get_packages_result = StartPage.api_call(self, usrdef_sship, 443, 'show-packages', get_packages_data, sid)
        allpackagelist = []
        for package in get_packages_result["packages"]:
            allpackagelist.append(package["name"])
        #Package Dropdown
        defaultpackage = StringVar(self)
        defaultpackage.set("Select Package")
        packagemenu = OptionMenu(self, defaultpackage, *allpackagelist)
        packagemenu.grid(row=1, column=0)

        #Button to retrieve layers from package
        showrulebaseb = ttk.Button(self, text="Get Layers", command=lambda: self.getlayers(defaultpackage.get()))
        showrulebaseb.grid(row=2, column=1)

    def getlayers(self, package):
        get_layers_data = {'name':package}
        get_layers_result = StartPage.api_call(self, usrdef_sship, 443, 'show-package', get_layers_data, sid)
        alllayerslist = []
        #print (get_layers_result)
        for layer in get_layers_result["access-layers"]:
            alllayerslist.append(layer["name"])
        #Layer Dropdown
        defaultlayer = StringVar(self)
        defaultlayer.set("Select Layer")
        layermenu = OptionMenu(self, defaultlayer, *alllayerslist)
        layermenu.grid(row=2, column=0)

        #Button to retrieve rulebase
        showrulebaseb = ttk.Button(self, text="Export Rules", command=lambda: self.exportrules(package, defaultlayer.get()))
        showrulebaseb.grid(row=3, column=0)

    #Method to get export rules
    def exportrules(self, package, layer):
        #Retrieve Rulebase
        show_rulebase_data = {"offset":0, "package":package, "name":layer, "details-level":"standard", "use-object-dictionary":"true"}
        show_rulebase_result = StartPage.api_call(self, usrdef_sship, 443, 'show-access-rulebase', show_rulebase_data ,sid)
        #Create Output File
        rulebaseexport = open(("exportedrules.csv"), "w+")
        #Parse values for each rule
        for rule in show_rulebase_result["rulebase"]:
            countersrc = 0
            counterdst = 0
            countersrv = 0
            #String, String, List, List, List, String
            ### NAME CAN BE EMPTY ###
            if 'name' in rule:
                name = rule["name"]
            else:
                name = "ASSIGN NAME"
            num = rule["rule-number"]
            src = rule["source"]
            dst = rule["destination"]
            srv = rule["service"]
            act = rule["action"]
            #Parse Object Ditcionary to replace UID with Name
            for obj in show_rulebase_result["objects-dictionary"]:
                if name == obj["uid"]:
                    name = obj["name"]
            #Parse Object Ditcionary to replace UID with Name
            for obj in show_rulebase_result["objects-dictionary"]:
                if num == obj["uid"]:
                    num = obj["name"]
            #Parse Object Ditcionary to replace UID with Name: Source
            if len(src) == 1:
                for obj in show_rulebase_result["objects-dictionary"]:
                    if src[0] == obj["uid"]:
                        src = obj["name"]
            else:
                for srcobj in src:
                    for obj in show_rulebase_result["objects-dictionary"]:
                        if srcobj == obj["uid"]:
                            src[countersrc] = obj["name"]
                            countersrc = countersrc + 1
            #Parse Object Ditcionary to replace UID with Name: Destination
            if len(dst) == 1:
                for obj in show_rulebase_result["objects-dictionary"]:
                    if dst[0] == obj["uid"]:
                        dst = obj["name"]
            else:
                for dstobj in dst:
                    for obj in show_rulebase_result["objects-dictionary"]:
                        if dstobj == obj["uid"]:
                            dst[counterdst] = obj["name"]
                            counterdst = counterdst + 1
            #Parse Object Ditcionary to replace UID with Name: Service
            if len(srv) == 1:
                for obj in show_rulebase_result["objects-dictionary"]:
                    if srv[0] == obj["uid"]:
                        srv = obj["name"]
            else:
                for srvobj in srv:
                    for obj in show_rulebase_result["objects-dictionary"]:
                        if srvobj == obj["uid"]:
                            srv[countersrv] = obj["name"]
                            countersrv = countersrv + 1
            #Parse Object Ditcionary to replace UID with Name
            for obj in show_rulebase_result["objects-dictionary"]:
                if act == obj["uid"]:
                    act = obj["name"]
            #Write Rule Number and Name
            rulebaseexport.write(str(num) + ',' + name + ',')
            #Write Source, delimit multiple with ;
            if isinstance(src, str) == True:
                rulebaseexport.write(src + ',')
            else:
                for srcele in src[0:-1]:
                    rulebaseexport.write(srcele + ';')
                rulebaseexport.write(src[-1] + ',')
            #Write Destination, delimit multiple with ;
            if isinstance(dst, str) == True:
                rulebaseexport.write(dst + ',')
            else:
                for dstele in dst[0:-1]:
                    rulebaseexport.write(dstele + ';')
                rulebaseexport.write(dst[-1] + ',')
            #Write Service, delimit multiple with ;
            if isinstance(srv, str) == True:
                rulebaseexport.write(srv + ',')
            else:
                for srvele in srv[0:-1]:
                    rulebaseexport.write(srvele + ';')
                rulebaseexport.write(srv[-1] + ',')
            #Write Action and \n
            rulebaseexport.write(act + '\n')
        rulebaseexport.close()
        messagebox.showinfo("Export Rulebase", "PLACEHOLDER")

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Rulebase")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve packages
        getpackagesb = ttk.Button(self, text="Get Packages", command=lambda: self.getpackages())
        getpackagesb.grid(row=1, column=1)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=4, column=0)

#Class to add runscript functionality
class RunScript(tk.Frame):

    #Method to retrieve valid gateways and servers
    def gettargets(self):
        #Retrieve Targets
        get_targets_data = {'offset':0}
        get_targets_result = StartPage.api_call(self, usrdef_sship, 443, 'show-gateways-and-servers', get_targets_data ,sid)
        targetslist = []
        for obj in get_targets_result["objects"]:
            targetslist.append(obj["name"])
        #Target Dropdown
        defaulttarget = StringVar(self)
        defaulttarget.set("Select Target")
        targetmenu = OptionMenu(self, defaulttarget, *targetslist)
        targetmenu.grid(row=1, column=0)

        #Script Name
        scriptname_l = ttk.Label(self, text="Script Name")
        scriptname_l.configure(background="#494949", foreground="#f44242")
        scriptname_l.grid(row=2, column=0, sticky=E)
        scriptname_e = Entry(self, bd=5)
        scriptname_e.grid(row=2, column=1)
        scriptname_e.configure(background="#ffffff")

        #Script Command
        scriptcommand_l = ttk.Label(self, text="Script Command")
        scriptcommand_l.configure(background="#494949", foreground="#f44242")
        scriptcommand_l.grid(row=3, column=0, sticky=E)
        scriptcommand_e = Entry(self, bd=5)
        scriptcommand_e.grid(row=3, column=1)
        scriptcommand_e.configure(background="#ffffff")

        #Button to runscript
        runthescriptb = ttk.Button(self, text="Run Script", command=lambda: self.runscript(defaulttarget.get(), scriptname_e.get(), scriptcommand_e.get()))
        runthescriptb.grid(row=4, column=0)

    #Method to run command
    def runscript(self, target, name, command):
        run_script_data = {'script-name':name, 'script':command, 'targets':target}
        get_targets_result = StartPage.api_call(self, usrdef_sship, 443, 'run-script', run_script_data , sid)
        for line in get_targets_result["tasks"]:
            taskid = line["task-id"]
        time.sleep(5)
        taskid_data = {'task-id':taskid, 'details-level':'full'}
        taskid_result = StartPage.api_call(self, usrdef_sship, 443, 'show-task', taskid_data , sid)
        for line in taskid_result["tasks"]:
            taskresult = line["task-details"][0]["statusDescription"]
        messagebox.showinfo("Run Script Output", taskresult)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Run Script")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve targets
        getpackagesb = ttk.Button(self, text="Get Targets", command=lambda: self.gettargets())
        getpackagesb.grid(row=1, column=1)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=2)

class dthomas(tk.Frame):

    def allobjects(self, ip):
        all_hosts_data = {'offset':0, 'details-level':'full'}
        all_hosts_result = StartPage.api_call(self, usrdef_sship, 443, 'show-hosts', all_hosts_data, sid)
        for nat in all_hosts_result["objects"]:
            if 'ipv4-address' in nat["nat-settings"]:
                host = nat["name"]
                found = nat["nat-settings"]["ipv4-address"]
                if ip == found:
                    messagebox.showinfo("Results", ("Host %s contains the NAT IP" % host))
        all_networks_data = {'offset':0, 'details-level':'full'}
        all_networks_result = StartPage.api_call(self, usrdef_sship, 443, 'show-networks', all_networks_data, sid)
        for nat in all_networks_result["objects"]:
            if 'ipv4-address' in nat["nat-settings"]:
                network = nat["name"]
                found = nat["nat-settings"]["ipv4-address"]
                if ip == found:
                    messagebox.showinfo("Results", ("Network %s contains the NAT IP" % network))

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Get All Objects")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Search for IP
        search_l = ttk.Label(self, text="IP to Search")
        search_l.configure(background="#494949", foreground="#f44242")
        search_l.grid(row=1, column=0, sticky=E)
        search_e = Entry(self, bd=5)
        search_e.grid(row=1, column=1)
        search_e.configure(background="#ffffff")

        #Button to retrieve all objects
        getpackagesb = ttk.Button(self, text="Get Objects", command=lambda: self.allobjects(search_e.get()))
        getpackagesb.grid(row=2, column=1)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)
#Call Main Frame
if __name__ == "__main__":
    app = apiapp()
    app.mainloop()
