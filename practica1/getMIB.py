
from pysnmp.hlapi import *

def getMIBagent(community,host,port):

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')), #sysname
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')), #sysdescr
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')), #ifnumber
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')), #sysuptime 
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')), #syslocation physical loc
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')) #syscontact
            )
    )
    #	1.3.6.1.2.1.4.20.1.3 know ip 

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        return varBinds

