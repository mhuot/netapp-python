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

vols = []
tag = None
while True:
  print "Must be true"
  vol_info = NaElement('volume-get-iter')
  if tag:
    vol_info.add_new_child('tag', tag, True)
  
  result = s.invoke_successfully(vol_info, True)
  if result.get_child_by_name('num-records') and int(result.get_child_content('num-records')) >= 1:
    attr_list = result.get_child_by_name('attributes-list')
    vols.extend(attr_list.get_children())
  tag = result.get_child_content('next-tag')
  
  if tag is None:
    break

for vol in vols:
  print vol.get_child_by_name('volume-id-attributes').get_child_by_name('name').to_string()
