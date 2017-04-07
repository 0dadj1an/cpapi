##Import Paramiko Client
from paramiko import client
#Import Things
import sys, re, time
#Import json
import json
#Import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *

#Class for ssh session and sending commands
class ssh:
    client = None

    def __init__(self, address, username, password):
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)

    def sendCommand(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                time.sleep(2)
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata

                    return (str(alldata, "utf8"))
        else:
            print ("Connection not opened.")

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
        for F in (StartPage, AddHost, AddNetwork, ShowHosts):
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
        label = ttk.Label(self, text="Available API Functions")
        label.configure(background="#494949", foreground="#f44242")
        label.grid(row=0)

        #Button to call add host window
        addhostb = ttk.Button(self, text="ADD HOST", command=lambda: controller.show_frame("AddHost"))
        addhostb.grid(row=1)

        #Button to call add network window
        addnetworkb = ttk.Button(self, text="ADD NETWORK", command=lambda: controller.show_frame("AddNetwork"))
        addnetworkb.grid(row=2)

        #Button to call show hosts window
        showhostsb = ttk.Button(self, text="SHOW HOSTS", command=lambda: controller.show_frame("ShowHosts"))
        showhostsb.grid(row=3)

#Class for add host functionality
class AddHost(tk.Frame):

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Add Host")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0)

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

        #Host Name
        hostname_l = ttk.Label(self, text = "Host Name", background="#494949", foreground="#f44242")
        hostname_l.grid(row=4, column=0, sticky=E)
        hostname_e = Entry(self, bd=5)
        hostname_e.grid(row=4, column=1)
        hostname_e.configure(background="#ffffff")

        #Host IP
        hostip_l = ttk.Label(self, text = "Host IP", background="#494949", foreground="#f44242")
        hostip_l.grid(row=5, column=0, sticky=E)
        hostip_e = Entry(self, bd=5)
        hostip_e.grid(row=5, column=1)
        hostip_e.configure(background="#ffffff")

        #Host Color
        hostcolor_l = ttk.Label(self, text="Host Color", background="#494949", foreground="#f44242")
        hostcolor_l.grid(row=6, column=0, sticky=E)
        defaultcolor = StringVar(self)
        defaultcolor.set("black")
        hostcolormenu = OptionMenu(self, defaultcolor, "black", "blue", "cyan", "gold", "green", "red", "orange", "yellow")
        hostcolormenu.grid(row=6, column=1)

        #Button to run command
        runapi = ttk.Button(self, text="Add Host", command = lambda: addhost())
        runapi.grid(row=3, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=4, column=2)

        #Method for adding a single host object
        def addhost():
            usrdef_sship = sship_e.get()
            usrdef_username = username_e.get()
            usrdef_pass = pass_e.get()
            hostname = hostname_e.get()
            hostip = hostip_e.get()
            hostcolor = defaultcolor.get()
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli login user " + usrdef_username + " password " + usrdef_pass + " > session.txt")
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli add host name " + hostname + " ipv4-address " + hostip + " color " + hostcolor + " -s session.txt")
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli publish -s session.txt ")

#Class for add network functionality
class AddNetwork(tk.Frame):

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Add Network")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0)

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

        #Network Name
        netname_l = ttk.Label(self, text = "Network Name", background="#494949", foreground="#f44242")
        netname_l.grid(row=4, column=0, sticky=E)
        netname_e = Entry(self, bd=5)
        netname_e.grid(row=4, column=1)
        netname_e.configure(background="#ffffff")

        #Network Address
        netaddr_l = ttk.Label(self, text = "Network Subnet", background="#494949", foreground="#f44242")
        netaddr_l.grid(row=5, column=0, sticky=E)
        netaddr_e = Entry(self, bd=5)
        netaddr_e.grid(row=5, column=1)
        netaddr_e.configure(background="#ffffff")

        #Network Mask
        netmask_l = ttk.Label(self, text = "Mask Length in CIDR", background="#494949", foreground="#f44242")
        netmask_l.grid(row=6, column=0, sticky=E)
        netmask_e = Entry(self, bd=5)
        netmask_e.grid(row=6, column=1)
        netmask_e.configure(background="#ffffff")

        #Button to run command
        runapi = ttk.Button(self, text="Add Network", command = lambda: addnetwork())
        runapi.grid(row=3, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=4, column=2)

        #Method for adding a single network object
        def addnetwork():
            usrdef_sship = sship_e.get()
            usrdef_username = username_e.get()
            usrdef_pass = pass_e.get()
            netname = netname_e.get()
            netaddr = netaddr_e.get()
            netmask = netmask_e.get()
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli login user " + usrdef_username + " password " + usrdef_pass + " > session.txt")
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli add network name " + netname + " subnet " + netaddr + " mask-length " + netmask + " -s session.txt")
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli publish -s session.txt ")

class ShowHosts(tk.Frame):

    def __init__(self, parent, controller):

        #Style Configuration for page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#494949")
        addhostlabel = ttk.Label(self, text="Show Hosts")
        addhostlabel.configure(background="#494949", foreground="#f44242")
        addhostlabel.grid(row=0, column=0)

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

        #Button to run command
        runapi = ttk.Button(self, text="Show Hosts", command = lambda: showhosts())
        runapi.grid(row=1, column=2)

        #Button to return to apiapp
        button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=2)

        def showhosts():
            usrdef_sship = sship_e.get()
            usrdef_username = username_e.get()
            usrdef_pass = pass_e.get()
            ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli login user " + usrdef_username + " password " + usrdef_pass + " > session.txt")
            allhosts = ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli show hosts --format json -s session.txt")
            json_hosts = json.loads(allhosts)
            print (json_hosts["objects"][0]["name"])

if __name__ == "__main__":
    app = apiapp()
    app.mainloop()
