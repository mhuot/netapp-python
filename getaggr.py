import sys
import xml.etree.ElementTree as ET
from netapp_lib.api.zapi.zapi import NaElement
from netapp_lib.api.zapi.zapi import NaServer

s = NaServer("192.168.1.31")
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_api_version(1,120)
s.set_style("basic_auth")
s.set_username("ansible")
s.set_password("4N51bl3!")

api = NaElement("aggr-get-iter")


xo = s.invoke_elem(api)
print xo
#if (xo.results_status() == "failed") :
#  print ("Error:\n")
#  print (xo.sprintf())
#  sys.exit (1)

#print ("Received:\n")
#print (xo.get_content().sprintf())
ns = {'netapp': 'http://www.netapp.com/filer/admin'}
root = ET.fromstring(xo.to_string())

#print xo.to_string()
print root.tag

for attrlist in root.findall('netapp:attributes-list', ns):
  print attrlist.tag
  for aggrattr in attrlist.findall('netapp:aggr-attributes', ns):
    aggrname = aggrattr.find('netapp:aggregate-name', ns)
    print aggrname.text
    for nodes in aggrattr.findall('netapp:nodes', ns):
      nodename = nodes.find('netapp:node-name', ns)
      print nodename.text
