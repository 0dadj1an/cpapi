#Import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
#Import cpapicall
from cpapicall import allcalls

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
            ImportRules, ExportRules, RunScript, PutFile, FindNat):
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
        sessionb = ttk.Button(self, text="Connect", command=lambda: allcalls.login(sship_e.get(), username_e.get(), pass_e.get()))
        sessionb.grid(row=1, column=2)

        #Button to publish session
        publishb = ttk.Button(self, text="Publish", command=lambda: allcalls.publish())
        publishb.grid(row=2, column=2)

        #Button to logout session
        logoutb = ttk.Button(self, text="Logout", command=lambda: allcalls.logout())
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

        #Button to call put-file window
        runscriptb = ttk.Button(self, text="Put File", command=lambda: controller.show_frame("PutFile"))
        runscriptb.grid(row=9, column=1)

        #Butto to call findnat window
        dthomb = ttk.Button(self, text="Find NAT", command=lambda: controller.show_frame("FindNat"))
        dthomb.grid(row=9, column=2)

#Class for add host functionality
class AddHost(tk.Frame):

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
        runapi = ttk.Button(self, text="Add Host", command=lambda: allcalls.addhost(hostname_e.get(), hostip_e.get(), defaultcolor.get()))
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Class for add network functionality
class AddNetwork(tk.Frame):

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
        netmask_l = ttk.Label(self, text = "Mask-Length", background="#494949", foreground="#f44242")
        netmask_l.grid(row=3, column=0, sticky=E)
        netmask_e = Entry(self, bd=5)
        netmask_e.grid(row=3, column=1)
        netmask_e.configure(background="#ffffff")

        #Host Color
        networkcolor_l = ttk.Label(self, text="Network Color", background="#494949", foreground="#f44242")
        networkcolor_l.grid(row=4, column=0, sticky=E)
        defaultcolor = StringVar(self)
        defaultcolor.set("black")
        netowrkcolormenu = OptionMenu(self, defaultcolor, "black", "blue", "cyan", "gold", "green", "red", "orange", "yellow")
        netowrkcolormenu.grid(row=4, column=1)

        #Button to run command
        runapi = ttk.Button(self, text="Add Network", command = lambda: allcalls.addnetwork(netname_e.get(), netaddr_e.get(), netmask_e.get(), defaultcolor.get()))
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Class for add network functionality
class AddGroup(tk.Frame):

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
        runapi = ttk.Button(self, text="Add Group", command = lambda: allcalls.addgroup(groupname_e.get()))
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Class for adding objects to a group functionality
class ObjectToGroup(tk.Frame):

    #Method to retrieve hosts,networks,groups
    def gethostnetgroup(self):
        #Create list for each type
        allhostlist = []
        allnetlist = []
        allgrouplist = []
        #API Call for each type
        show_hosts_result = allcalls.getallhosts()
        show_nets_result = allcalls.getallnetworks()
        show_groups_result = allcalls.getallgroups()
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
        hosttogroupb = ttk.Button(self, text="Add Host", command=lambda: allcalls.addhostgroup(defaulthost.get(), defaultgroup.get()))
        hosttogroupb.grid(row=2, column=2)

        #Button to add network to group
        nettogroupb = ttk.Button(self, text="Add Network", command=lambda: allcalls.addnetgroup(defaultnet.get(), defaultgroup.get()))
        nettogroupb.grid(row=3, column=2)

        #Button to add group to group
        grouptogroup = ttk.Button(self, text="Add Group", command=lambda: allcalls.addgroupgroup(defaultaddgroup.get(), defaultgroup.get()))
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
        imphostb = ttk.Button(self, text="Import", command=lambda: allcalls.importhosts(file_e.get()))
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

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Hosts")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to export hosts
        exphostb = ttk.Button(self, text="Export Hosts", command=lambda: allcalls.exporthosts())
        exphostb.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)

#Class for adding importnetwork functionality
class ImportNetworks(tk.Frame):

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
        exphostb = ttk.Button(self, text="Import Networks", command=lambda: allcalls.importnetworks(file_e.get()))
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

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Networks")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to export networks
        exphostb = ttk.Button(self, text="Export Networks", command=lambda: allcalls.exportnetworks())
        exphostb.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)

#Class for adding importgroup functionality
class ImportGroups(tk.Frame):

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
        exphostb = ttk.Button(self, text="Import Groups", command=lambda: allcalls.importgroups(file_e.get()))
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

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Groups")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to export groups
        exphostb = ttk.Button(self, text="Export Groups", command=lambda: allcalls.exportgroups())
        exphostb.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=1)

#Class for adding importrule functionality
class ImportRules(tk.Frame):

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
        exphostb = ttk.Button(self, text="Import Rulebase", command=lambda: allcalls.importrules(file_e.get()))
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

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Export Rulebase")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve packages
        getpackagesb = ttk.Button(self, text="Get Packages", command=lambda: allcalls.getpackages())
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

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Run Script")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve targets
        getpackagesb = ttk.Button(self, text="Get Targets", command=lambda: allcalls.gettargets())
        getpackagesb.grid(row=1, column=1)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=2)

#Class to add putfile functionality
class PutFile(tk.Frame):

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

        #File Location
        fileloc_l = ttk.Label(self, text="File Path")
        fileloc_l.configure(background="#494949", foreground="#f44242")
        fileloc_l.grid(row=2, column=0, sticky=E)
        fileloc_e = Entry(self, bd=5)
        fileloc_e.grid(row=2, column=1)
        fileloc_e.configure(background="#ffffff")

        #File Name
        filename_l = ttk.Label(self, text="File Name")
        filename_l.configure(background="#494949", foreground="#f44242")
        filename_l.grid(row=3, column=0, sticky=E)
        filename_e = Entry(self, bd=5)
        filename_e.grid(row=3, column=1)
        filename_e.configure(background="#ffffff")

        #File Contents
        filecontents_l = ttk.Label(self, text="File Contents")
        filecontents_l.configure(background="#494949", foreground="#f44242")
        filecontents_l.grid(row=4, column=0, sticky=E)
        filecontents_e = Entry(self, bd=5)
        filecontents_e.grid(row=4, column=1)
        filecontents_e.configure(background="#ffffff")

        #Button to run putfile
        runthescriptb = ttk.Button(self, text="Put File", command=lambda: self.putfile(defaulttarget.get(), fileloc_e.get(), filename_e.get(), filecontents_e.get()))
        runthescriptb.grid(row=5, column=0)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Put File")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve targets
        getpackagesb = ttk.Button(self, text="Get Targets", command=lambda: allcalls.gettargets())
        getpackagesb.grid(row=1, column=1)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=2)

#Class to add find object with associated NAT ip functionality
class FindNat(tk.Frame):

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Search Objects for associated NAT IP")
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
        getpackagesb = ttk.Button(self, text="Search Objects", command=lambda: allcalls.findnat(search_e.get()))
        getpackagesb.grid(row=2, column=1)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

#Call Main Frame
if __name__ == "__main__":
    app = apiapp()
    app.mainloop()
