#Import Things
import sys, re, time, json, requests
#Import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *

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
        for F in (StartPage, AddHost, AddNetwork, AddGroup, ObjectToGroup, ImportHosts, ExportHosts, ImportNetworks, ExportNetworks):
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
        sid = (response["sid"])

    #Method to publish api session
    def publish(self):
        publish_result = self.api_call(usrdef_sship, 443, 'publish', {} ,sid)

    #Method to logout over api
    def logout(self):
        logout_result = self.api_call(usrdef_sship, 443,"logout", {},sid)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        label = ttk.Label(self, text="Credentials for Session")
        label.configure(background="#494949", foreground="#f44242")
        label.grid(row=0, columnspan=2)

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
        addhosttogroup.grid(row=5, column=0, columnspan=3)

        #Button to call add host window
        addhostb = ttk.Button(self, text="Add Host", command=lambda: controller.show_frame("AddHost"))
        addhostb.grid(row=6)

        #Button to call add network window
        addnetworkb = ttk.Button(self, text="Add Network", command=lambda: controller.show_frame("AddNetwork"))
        addnetworkb.grid(row=6, column=1)

        #Button to call add group window
        addgroupb = ttk.Button(self, text="Add Group", command=lambda: controller.show_frame("AddGroup"))
        addgroupb.grid(row=6, column=2)

        #Button to call import hosts window
        imphostb = ttk.Button(self, text="Import Hosts", command=lambda: controller.show_frame("ImportHosts"))
        imphostb.grid(row=7, column=0)

        #Button to call export hosts window
        exphostsb = ttk.Button(self, text="Export Hosts", command=lambda: controller.show_frame("ExportHosts"))
        exphostsb.grid(row=8, column=0)

        #Button to call import networks
        impnetsb = ttk.Button(self, text="Import Networks", command=lambda: controller.show_frame("ImportNetworks"))
        impnetsb.grid(row=7, column=1)

        #Button to call export networks
        expnetsb = ttk.Button(self, text="Export Networks", command=lambda: controller.show_frame("ExportNetworks"))
        expnetsb.grid(row=8, column=1)

#Class for add host functionality
class AddHost(tk.Frame):

    #Method for adding a host object
    def addhost(self, hostname, hostip, hostcolor):
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
        new_host_result = StartPage.api_call(self, usrdef_sship, 443,'add-host', new_host_data ,sid)

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
        netaddr_l = ttk.Label(self, text = "Network Subnet", background="#494949", foreground="#f44242")
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

    #Method for adding a network object
    def addgroup(self, groupname):
        new_group_data = {'name':groupname}
        new_group_result = StartPage.api_call(self, usrdef_sship, 443,'add-group', new_group_data ,sid)

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

    def addnetgroup(self, netname, groupname):
        addnetgroup_data = {'name':netname, 'groups':groupname}
        addnetgroup_result = StartPage.api_call(self, usrdef_sship, 443, 'set-network', addnetgroup_data, sid)

    def addgroupgroup(self, addgroupname, groupname):
        addgroup_data = {'name':addgroupname, 'groups':groupname}
        addgroupgroup_result = StartPage.api_call(self, usrdef_sship, 443, 'set-group', addgroup_data, sid)

    #Method to retrieve db hosts and Groups
    def gethostnetgroup(self):
        allhostlist = []
        allnetlist = []
        allgrouplist = []
        show_hosts_data = {'limit':50, 'offset':0, 'details-level':'standard'}
        show_hosts_result = StartPage.api_call(self, usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        show_groups_data = {'limit':50, 'offset':0, 'details-level':'standard'}
        show_groups_result = StartPage.api_call(self, usrdef_sship, 443, 'show-groups', show_groups_data, sid)
        show_nets_data = {'limit':50, 'offset':0, 'details-level':'standard'}
        show_nets_result = StartPage.api_call(self, usrdef_sship, 443, 'show-networks', show_nets_data, sid)
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
        allgroup2.grid(row=5, column=0, sticky=E)
        defaultgroup = StringVar(self)
        defaultgroup.set("Target Group")
        groupmenu = OptionMenu(self, defaultgroup, *allgrouplist)
        groupmenu.grid(row=5, column=1)

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

class ImportHosts(tk.Frame):

    #Method to import host from csv file
    def importhosts(self, filename):
        csvhosts = open(filename, "r").read().split()
        for line in csvhosts:
            apiprep = line.split(',')
            AddHost.addhost(self, apiprep[0], apiprep[1], "black")

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

class ExportHosts(tk.Frame):

    #Method to export host to csv file
    def exporthosts(self):
        show_hosts_data = {'offset':0, 'details-level':'full'}
        show_hosts_result = StartPage.api_call(self, usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        hostexportfile = open(("exportedhosts.csv"), "w+")
        for host in show_hosts_result["objects"]:
            hostexportfile = open(("exportedhosts.csv"), "a")
            hostexportfile.write(host["name"] + "," + host["ipv4-address"] + "\n")

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

class ImportNetworks(tk.Frame):

    def importnetworks(self, filename):
        csvnets = open(filename, "r").read().split()
        for line in csvnets:
            apiprep = line.split(',')
            AddNetwork.addnetwork(self, apiprep[0], apiprep[1], apiprep[2])

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

class ExportNetworks(tk.Frame):

    #Method to export host to csv file
    def exportnetworks(self):
        show_networks_data = {'offset':0, 'details-level':'full'}
        show_networks_result = StartPage.api_call(self, usrdef_sship, 443, 'show-networks', show_networks_data ,sid)
        networksexportfile = open(("exportednetworks.csv"), "w+")
        for network in show_networks_result["objects"]:
            networksexportfile = open(("exportednetworks.csv"), "a")
            networksexportfile.write(network["name"] + "," + str(network["subnet4"]) + "," + str(network["mask-length4"]) + "\n")

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

if __name__ == "__main__":
    app = apiapp()
    app.mainloop()
