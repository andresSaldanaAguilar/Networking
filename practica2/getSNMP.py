
from pysnmp.hlapi import *

def request(community,host,oid,port):

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        #print(errorIndication)
        #aqui se maneja la no respuesta del agente
        print("Sin respuesta de "+host)
        resultado = ""
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split('=')[1]
    return resultado
    
def requestRT(community,host,oid,port):

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        #print(errorIndication)
        #aqui se maneja la no respuesta del agente
        print("Sin respuesta de "+host)
        resultado = ""
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2]
            if resultado == "No":
                resultado = ""
                
    return resultado
    
def requestWalk(community,host,oid,port):
    
    objects = []

    for(errorIndication,
            errorStatus,
            errorIndex,
            varBinds
    ) in nextCmd(SnmpEngine(), 
            CommunityData(community),
            UdpTransportTarget((host, port)),
            ContextData(),                                                           
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False
    ):
            if errorIndication:
                 resultado = ""
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                for oid, value in varBinds:
                    objects.append(oid.prettyPrint()[-1:])
                #print(objects)
    return objects
