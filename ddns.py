# websupport.sk DNS remote conf script

import hmac
import hashlib
import time
import requests
import base64
import datetime
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
from urllib2 import urlopen
import socket
import json
from collections import OrderedDict
import ast
import syslog
from ddns_conf import *

# prepare and make request for desired record_id
def update_request(record_id, name, new_ip, ttl):
    # Websupport REST API section
    method = 'PUT'
    path = '/v1/user/%s/zone/%s/record/%s' % (user_id, domain, record_id)
    jdata = {}
    jdata['name'] = name
    jdata['content'] = new_ip
    jdata['ttl'] = ttl
    # prepare data for sending - separators, single quote marks
    data = json.dumps(OrderedDict([("name", name), ("content", new_ip), ("ttl", ttl)]), separators=(',', ':'),)
    data = ast.literal_eval(data)

    timestamp = int(time.time())
    canonicalRequest = '%s %s %s' % (method, path, timestamp)
    signature = hmac.new(secret, canonicalRequest.encode('utf-8'), hashlib.sha1).hexdigest()

    headers = {
        'Authorization': 'Basic %s' % (base64.b64encode('%s:%s' % (apiKey, signature))),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Date': datetime.datetime.fromtimestamp(timestamp).isoformat()
    }

    # WS REST API change IP
    result = requests.put('%s%s' % (api, path), headers=headers, json=data).content
    return result

def send_mail(public_ip, body_msg):
    # Mailing info
    # Account Information
    today = datetime.date.today()  # Get current time/date
    now = datetime.datetime.now() # Get current time

    # connection for mailing
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)

    # Creates the text, subject, 'from', and 'to' of the message.
    #msg = MIMEText('actual public IP: %s' %  public_ip)
    msg = MIMEText(body_msg)
    msg['Subject'] = 'Delah IP Info: change of p_IP on %s %s' %(now.strftime('%H:%M'), today.strftime('%d-%b-%Y'))
    msg['From'] = gmail_user
    msg['To'] = to
    # Send the message
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    # Closes the smtp server.
    smtpserver.quit()

# Obtaining IP reated info
my_ip = urlopen(get_plain_IP).read()
last_ip = socket.gethostbyname(www_domain)

# main code
#print my_ip
#print last_ip
result = ''
if my_ip != last_ip:
    for i in record_ids:
        result += update_request(i, record_ids[i], my_ip, global_ttl) + "\n"
    send_mail(my_ip, result)
    syslog.syslog(syslog.LOG_INFO, result)    
else:
        pass
