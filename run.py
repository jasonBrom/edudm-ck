# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
import os
import socks
import socket
from stem import Signal
from stem.control import Controller

def check_domain_sku_status(domain):
    x = requests.get("https://signup.microsoft.com/signup?sku=Education")
    soup = BeautifulSoup(x.text, 'html.parser')
    match = soup.find('input', id='WizardState')
    while match is None:
        controller.signal(Signal.NEWNYM)
        time.sleep(10)
        x = requests.get("https://signup.microsoft.com/signup?sku=Education")
        soup = BeautifulSoup(x.text, 'html.parser')
        match = soup.find('input', id='WizardState')
        WizardState = match["value"]
    else:
        WizardState = match["value"]
    data = {
        "StepsData.Email": "fadaw@" + domain,
        "MessageId": "GenericError",
        "BackgroundImageUrl":"",
        "SkuId": "Education",
        "Origin": "",
        "IsAdminSignup": False,
        "CurrentWedcsTag": "/Signup/CollectEmail",
        "WizardState": WizardState,
        "WizardFullViewRendered": True,
        "ShowCookiesDisclosureBanner": False,
        "X-Requested-With": "XMLHttpRequest"
    }
    x = requests.post("https://signup.microsoft.com/signup/indexinternal?sku=Education", json=data)
    if 'id="sku_314c4481-f395-4525-be8b-2ec4bb1e9d91"' in x.text:
        print("The domain: " + domain + ". Can use for A1.")
        with open("domain_A1.txt", "a") as write:
            write.write(domain + "\n")
    elif 'id="sku_e82ae690-a2d5-4d76-8d30-7c6e01e6022e"' in x.text:
        print("The domain: " + domain + ". Can use for A1P.")
        with open("domain_A1P.txt", "a") as write:
            write.write(domain + "\n")
    else:
        print("The domain: " + domain + ". Can't do anything")

def get_domain_can_register(domain):
    url = "https://who.is/whois/" + domain
    x = requests.get(url)
    if "No match for" in x.text or "NOT FOUND" in x.text:
        return True
    else:
        return False

count = 0

controller = Controller.from_port(port=9151)
controller.authenticate()
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket

with open("nces.ed.gov.txt", 'r') as f:
    print(len(f.readlines()))
#yms=0

f = open("nces.ed.gov.txt")
line = f.readline()
while line:
    #print line,
    yms=print(line, end = '')
    line = f.readline()
    zcjc = get_domain_can_register(yms)
    if zcjc == True:
        check_domain_sku_status(domain)
    #time.sleep(0.01)

f.close()
