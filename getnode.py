import sys
import xml.etree.ElementTree as ET
from netapp_lib.api.zapi.zapi import NaElement
from netapp_lib.api.zapi.zapi import NaServer
import ssl
try:
  _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
  # Legacy Python that doesn't verify HTTPS certificates by default
  pass
else:
  # Handle target environment that doesn't support HTTPS verification
  ssl._create_default_https_context = _create_unverified_https_context

s = NaServer("192.168.1.31")
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_api_version(1,120)
s.set_style("basic_auth")
s.set_username("ansible")
s.set_password("4N51bl3!")

api = NaElement("system-node-get-iter")

xo = s.invoke_elem(api)

root = ET.fromstring(xo.to_string())

if root.get('status') == "passed":
  for attrlist in root.findall('{http://www.netapp.com/filer/admin}attributes-list'):
    for nodedetail in attrlist:
      nodename = nodedetail.find('{http://www.netapp.com/filer/admin}node')
      print nodename.text
else:
 print "Error: " + root.get('reason')
 sys.exit (1)