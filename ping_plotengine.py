#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author : obooklage
@date : 30/05/2021
@desc : plot in terminal ping reponses (ICMP) from host

A faire : que faire avec un ping = -1 ?

'''
import plotext as plt
import numpy as np
import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from packaging import version # check plotext version

colors = {"green":"\33[1;32;40m ", "yellow":"\033[1;33;40m ", "red":"\033[1;31;40m ", "purple":"\033[1;35;40m ", "white":"\033[1;37;40m ", "reset":"\33[0m"}
default_color = colors["green"]

def IsWindows():
    return(platform.system().lower() == "windows")

def PingTime(host):

    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    if IsWindows(): # Windows
        param = '-n'
    else: # Linux
        param = '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '2', host]
        
    if IsWindows():
        CREATE_NO_WINDOW = 0x08000000 # Nouveau
        p = subprocess.run(command, shell=False, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW) # Windows
    else: 
        p = subprocess.run(command, shell=False, stdout=subprocess.PIPE) # Linux

    #Windows
    if IsWindows():
        result = p.stdout.decode('cp1252') # .encode('utf-8') # encodage OEM 850
        result = result.replace("\r\n","\n")
        tab1 = result.split("\n")
        
        for i in tab1:
            if i.find("TTL") != -1:
                tab2 = i.split(" ")
                for j in tab2:
                        if j.find("temps") != -1: #Change to your language here !
                            k = j.split("=")
                            time = k[1];
                            return float(time)
    #Linux
    else:
        tab1 = p.stdout.decode('utf-8').split('\n')
        for i in tab1:
            if i.find("avg") != -1:
                j = i.split("=")
                k = j[1].split("/")
                return float(k[1])

    return -1

def PlotPing(host, list, maxdata):
    ping = PingTime(host)
    list = np.insert(list, 0, ping)
    list = np.delete(list, maxdata)
    plt.clp()
    plt.clt()
    plt.plot(list, fillx = True)
    if(ping < 30 ):
        color = colors["green"]
    elif ping < 80 :
        color = colors["yellow"]
    else:
        color = colors["red"]
    plt.title(default_color  + "ICMP reponse from " + host + color + str(ping) + default_color + "ms")

    if version.parse(plt.__version__) > version.parse("2.3.1"):
        plt.colorless()
    else:
        plt.nocolor() # in version 3.0.1, changed to colorless()

    plt.sleep(0.01)
    plt.show()
    return(list)

host = "google.com"
maxdata = 50 # 50 horizontal values max
pingslist = np.zeros(shape=(maxdata))
while True:
    pingslist = PlotPing(host, pingslist, maxdata)
    time.sleep(3)
