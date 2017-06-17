#Export
from cpapipackage.host import exporthosts
from cpapipackage.network import exportnetworks
from cpapipackage.group import exportgroups
from cpapipackage.policy import exportrules
from cpapipackage.policy import exportnat
from cpapipackage.service import exporttcpservices
from cpapipackage.service import exportudpservices

#Import
from cpapipackage.host import importhosts
from cpapipackage.network import importnetworks
from cpapipackage.group import importgroups
from cpapipackage.policy import importrules
from cpapipackage.policy import importnat
from cpapipackage.service import importtcpservice
from cpapipackage.service import importudpservice

#Variable for policy export
package = 'package'
layer = 'layer'

#Variable for filename imports
hostfile = 'exportedhosts.csv'
netfile = 'exportednetworks.csv'
groupfile = 'exportedgroups.csv'
rulesfile = 'exportedrules.csv'
natfile = 'exportednatrule.csv'
tcpfile = 'exportedtcpsrv.csv'
udpfile = 'exportedudpsrv.csv'

def exportgem(usrdef_sship, sid):
    exporthosts(usrdef_sship, sid)
    exportnetworks(usrdef_sship, sid)
    exportgroups(usrdef_sship, sid)
    exportrules(usrdef_sship, package, layer, sid)
    exportnat(usrdef_sship, package, sid)
    exporttcpservices(usrdef_sship, sid)
    exportudpservices(usrdef_sship, sid)

def importgem(usrdef_sship, hosts, nets, groups, policy, nat, tcp, udp, sid):
    importhosts(usrdef_sship, hostfile, sid)
    importnetworks(usrdef_sship, netfile, sid)
    importgroups(usrdef_sship, groupfile, sid)
    importrules(usrdef_sship, rulesfile, sid)
    importnat(usrdef_sship, natfile, sid)
    importtcpservice(usrdef_sship, tcpfile, sid)
    importudpservice(usrdef_sship, udpfile, sid)
