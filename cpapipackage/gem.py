#Import
from cpapipackage.host import exporthosts
from cpapipackage.network import exportnetworks
from cpapipackage.group import exportgroups
from cpapipackage.policy import exportrules
from cpapipackage.policy import exportnat
from cpapipackage.service import exporttcpservices
from cpapipackage.service import exportudpservices

#Variable for policy export
package = 'package'
layer = 'layer'

def exportgem(usrdef_sship, sid):
    exporthosts(usrdef_sship, sid)
    exportnetworks(usrdef_sship, sid)
    exportgroups(usrdef_sship, sid)
    exportrules(usrdef_sship, package, layer, sid)
    exportnat(usrdef_sship, package, sid)
    exporttcpservices(usrdef_sship, sid)
    exportudpservices(usrdef_sship, sid)

def importgem(usrdef_sship, hosts, nets, groups, policy, nat, tcp, udp, sid):
    pass
