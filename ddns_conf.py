# ddns_conf.py
# websupport.sk DNS remote conf script

import smtplib

# api info
api = 'https://rest.websupport.sk'
# place you API key 
apiKey = 'xxxx'
# place you API secret code 
secret = 'xxxx'

# domain related info
user_id = 'xxxx'
domain = 'xxxx.xx'
www_domain = 'www.xxxx.xx'

#desired TTL for all records
global_ttl = 666

# particular DNS records
# you may change them as you need - records must exist before (IDs)
record_ids = {
	'xxxx' : '@',
	'xxxx': '*',
	'xxxx':'www'
}

# get your plain public IP - specify service URL
get_plain_IP = 'http://ip.42.pl/raw'

# mail sending info - from gmail; if you want it
to = 'xx.xxxx@xxxx.xx;xx.xxxx@xxxx.xx' # Email to send to.
gmail_user = 'xx.xxxx@gmail.xom' # Email to send from. (MUST BE GMAIL)
gmail_password = 'xxxx' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.
