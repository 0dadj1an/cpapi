##Importing SSH
from paramiko import client
#Importing Arguments
import sys
#Import RegEx
import re
#Hopefully time.sleep(x) can solve the race condition.
import time
#Import tkinter
from tkinter import *
from tkinter import ttk

#Main Window
main = Tk()
main.iconbitmap('cpscanicon.ico')
main.wm_title("Check Point API Tool")
main.configure(background="#494949")

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

def addhost():
    usrdef_sship = sship_e.get()
    usrdef_username = username_e.get()
    usrdef_pass = pass_e.get()
    hostname = hostname_e.get()
    hostip = hostip_e.get()
    ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli login user " + usrdef_username + " password " + usrdef_pass + " > session.txt")
    ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli add host name " + hostname + " ipv4-address " + hostip + " -s session.txt")
    ssh(usrdef_sship, usrdef_username, usrdef_pass).sendCommand("mgmt_cli publish -s session.txt ")

#Button to run command
runapi = ttk.Button(main, text="Add Host", command = lambda: addhost())
runapi.grid(row=2, column=2)

#Collect IP for connection
sship_l = ttk.Label(main, text = "IP", background="#494949", foreground="#f44242")
sship_l.grid(row=0, column=0, sticky=E)
sship_e = Entry(main, bd=5)
sship_e.grid(row=0, column=1)
sship_e.configure(background="#ffffff")

#Collect Username for connection
username_l = ttk.Label(main, text = "Username", background="#494949", foreground="#f44242")
username_l.grid(row=1, column=0, sticky=E)
username_e = Entry(main, bd=5)
username_e.grid(row=1, column=1)
username_e.configure(background="#ffffff")

#Collect Password for connection
pass_l = ttk.Label(main, text = "Password",  background="#494949", foreground="#f44242")
pass_l.grid(row=2, column=0, sticky=E)
pass_e = Entry(main, bd=5, show="*")
pass_e.grid(row=2, column=1)
pass_e.configure(background="#ffffff")

#Host Name
hostname_l = ttk.Label(main, text = "Host Name", background="#494949", foreground="#f44242")
hostname_l.grid(row=3, column=0, sticky=E)
hostname_e = Entry(main, bd=5)
hostname_e.grid(row=3, column=1)
hostname_e.configure(background="#ffffff")

#Host IP
hostip_l = ttk.Label(main, text = "Host IP", background="#494949", foreground="#f44242")
hostip_l.grid(row=4, column=0, sticky=E)
hostip_e = Entry(main, bd=5)
hostip_e.grid(row=4, column=1)
hostip_e.configure(background="#ffffff")

#Need this to run
main.mainloop()
