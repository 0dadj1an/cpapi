#Import Things
import sys, re, time, json, requests
#Import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

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
        for F in (StartPage, AddHost, AddNetwork, HostToGroup):
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
        messagebox.showinfo("Login Response", json.dumps(response))

    #Method to publish api session
    def publish(self):
        publish_result = self.api_call(usrdef_sship, 443, 'publish', {} ,sid)
        messagebox.showinfo("Publish Response", json.dumps(publish_result))

    #Method to logout over api
    def logout(self):
        logout_result = self.api_call(usrdef_sship, 443,"logout", {},sid)
        messagebox.showinfo("Publish Response", json.dumps(logout_result))

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

        #Button to call add host window
        addhostb = ttk.Button(self, text="Add Host", command=lambda: controller.show_frame("AddHost"))
        addhostb.grid(row=4)

        #Button to call add network window
        addnetworkb = ttk.Button(self, text="Add Network", command=lambda: controller.show_frame("AddNetwork"))
        addnetworkb.grid(row=5)

        #Butto to call add host to group
        addhosttogroup = ttk.Button(self, text="Add Host To Group", command=lambda: controller.show_frame("HostToGroup"))
        addhosttogroup.grid(row=6)

#Class for add host functionality
class AddHost(tk.Frame):

    #Method for adding a host object
    def addhost(self, hostname, hostip, hostcolor):
        new_host_data = {'name':hostname, 'ipv4-address':hostip, 'color':hostcolor}
        new_host_result = StartPage.api_call(self, usrdef_sship, 443,'add-host', new_host_data ,sid)
        messagebox.showinfo("Add Host Response", json.dumps(new_host_result))

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
        messagebox.showinfo("Add Network Response", json.dumps(new_network_result))

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

class HostToGroup(tk.Frame):

    #Method to add host to group
    def addhostgroup(self, hostname, groupname):
        addhostgroup_data = {'name':hostname, 'groups':groupname}
        addhostgroup_result = StartPage.api_call(self, usrdef_sship, 443,'set-host', addhostgroup_data ,sid)
        print (json.dumps(new_network_result))

    #Method to retrieve db hosts and Groups
    def gethostgroup(self):
        allhostlist = []
        allgrouplist = []
        show_hosts_data = {'limit':50, 'offset':0, 'details-level':'standard'}
        show_hosts_result = StartPage.api_call(self, usrdef_sship, 443, 'show-hosts', show_hosts_data ,sid)
        show_groups_data = {'limit':50, 'offset':0, 'details-level':'standard'}
        show_groups_result = StartPage.api_call(self, usrdef_sship, 443, 'show-groups', show_groups_data, sid)
        for host in show_hosts_result["objects"]:
            allhostlist.append(host["name"])
        for group in show_groups_result["objects"]:
            allgrouplist.append(group["name"])
        allhost = ttk.Label(self, text="All Hosts", background="#494949", foreground="#f44242")
        allhost.grid(row=2, column=0, sticky=E)
        defaulthost = StringVar(self)
        defaulthost.set("Select Host")
        hostmenu = OptionMenu(self, defaulthost, *allhostlist)
        hostmenu.grid(row=2, column=1)
        allgroup = ttk.Label(self, text="All Groups", background="#494949", foreground="#f44242")
        allgroup.grid(row=3, column=0, sticky=E)
        defaultgroup = StringVar(self)
        defaultgroup.set("Select Group")
        groupmenu = OptionMenu(self, defaultgroup, *allgrouplist)
        groupmenu.grid(row=3, column=1)

        #Button to add host to group
        hosttogroupb = ttk.Button(self, text="Add", command=lambda: self.addhostgroup(defaulthost.get(), defaultgroup.get()))
        hosttogroupb.grid(row=1, column=1)

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Add Host to Group")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0, columnspan=2)

        #Button to retrieve objects
        runapi = ttk.Button(self, text="Get Objects", command=lambda: self.gethostgroup())
        runapi.grid(row=1, column=0)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=2)

if __name__ == "__main__":
    app = apiapp()
    app.mainloop()
