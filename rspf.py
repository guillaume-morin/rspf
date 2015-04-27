#!/usr/bin/python

import sys
import socket
import dns.resolver
import re

if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s domain\n" % sys.argv[0])
    sys.exit(1)

domain=sys.argv[1]

def getspf (domain):
   answers = dns.resolver.query(domain, 'TXT')
   for rdata in answers:
     for txt_string in rdata.strings:
       if txt_string.startswith('v=spf1'):
         return txt_string.replace('v=spf1','')

full_spf=getspf(domain)
print 'Initial SPF string : ', full_spf

while (full_spf.find('include:') > 0):
  for item in full_spf.split(' '):
    if item.startswith('include:'):
      sec_domain=item.replace('include:','')
      sec_spf=getspf(sec_domain)
      sec_spf=re.sub(' .all','',sec_spf)
      full_spf=full_spf.replace(item,sec_spf)
      print "SPF entry of %s : %s" % (sec_domain, sec_spf)

print 'Full SPF : ', full_spf

