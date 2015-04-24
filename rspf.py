#!/usr/bin/python

import sys
import socket
import dns.resolver

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] domain\n')
    sys.exit(1)

domain=sys.argv[1]

answers = dns.resolver.query(domain, 'TXT')
for rdata in answers:
  for txt_string in rdata.strings:
    if txt_string.startswith('v=spf1'):
      full_spf=txt_string.replace('v=spf1','')
      print 'Initial SPF string : ', full_spf

while (full_spf.find('include:') > 0):
  for item in full_spf.split(' '):
    if item.startswith('include:'):
      sec_domain=item.replace('include:','')
      answers = dns.resolver.query(sec_domain, 'TXT')
      for rdata in answers:
        for txt_string in rdata.strings:
          if txt_string.startswith('v=spf'):
            txt_string=txt_string.replace('v=spf1','')
            print "SPF entry of %s : %s" % (sec_domain, txt_string)
            full_spf=full_spf.replace(item,txt_string)

print 'Full SPF : ', full_spf

