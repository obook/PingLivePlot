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

def PingTime(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    if platform.system().lower()=='windows': # Windows
        param = '-n'
    else: # Linux
        param = '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '2', host]
        
    if platform.system().lower()=='windows':
        CREATE_NO_WINDOW = 0x08000000 # Nouveau
        p = subprocess.run(command, shell=False, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW) # Windows
    else: 
        p = subprocess.run(command, shell=False, stdout=subprocess.PIPE) # Linux

    #Windows
    if platform.system().lower()=='windows':
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
    plt.title("ICMP reponse from " + host + " " + str(ping) + " ms")
    plt.nocolor()
    plt.sleep(0.01)
    plt.show()
    return(list)

host = "google.com"
maxdata = 50 # 50 horizontal values max
pingslist = np.zeros(shape=(maxdata))
# xlabels = [str(i) + "π" for i in range(5)]
while True:
    pingslist = PlotPing(host, pingslist, maxdata)
    time.sleep(3)

