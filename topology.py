#!/usr/bin/python

'Shabir Ali: Wireless Fog-Mesh'

import os

from mininet.node import RemoteController
from mininet.wifi.node import OVSKernelAP
from mininet.log import setLogLevel, info
from mininet.wifi.link import wmediumd, mesh, physicalMesh
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.wmediumdConnector import interference

def topology():
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, accessPoint=OVSKernelAP,
                  link=wmediumd, wmediumd_mode=interference)
    os.system('service network-manager stop')

    info("*** Creating nodes\n")
    # Mesh Portal (USB Dongle) connect to real mesh network
    mpoint = net.addStation('mpoint', mac='20:50:00:00:00:01', position='50,150,0', ip='10.0.3.1/24', range=100, inNamespace=False)
    
    # End station
    sta1 = net.addStation('sta1', mac='20:50:00:00:00:02', position='50,50,0', ip='10.0.3.2/24', range=100)
    sta2 = net.addStation('sta2', mac='20:50:00:00:00:03', position='150,50,0', ip='10.0.3.3/24', range=100)
    sta3 = net.addStation('sta3', mac='20:50:00:00:00:04', position='250,300,0', ip='10.0.3.4/24', range=100)    
    sta4 = net.addStation('sta4', mac='20:50:00:00:00:05', position='350,200,0', ip='10.0.3.5/24', range=100)

     # Mesh Router/Relay Configuration
    mr1 = net.addStation('mr1', wlans=2, type='mesh', mac='20:50:00:00:00:06,20:50:00:00:00:07', ssid="ssid3,", mode="g", channel="1", position='200,100,0', ip='10.0.3.6/24')
    mr2 = net.addStation('mr2', wlans=2, type='mesh', mac='20:50:00:00:00:08,20:50:00:00:00:09', ssid="ssid4,", mode="g", channel="1", position='250,200,0', ip='10.0.3.7/24',)

    # Openflow Enabled Mesh Access Point
    ap1 = net.addAccessPoint('ap1', wlans=2, type='mesh', ssid="ssid1,", dpid='20:50:00:00:00:00:00:01', position='100,100,0', mode="g", channel="1")
    ap2 = net.addAccessPoint('ap2', wlans=2, type='mesh', ssid="ssid2,", dpid='20:50:00:00:00:00:00:02', position='300,250,0', mode='g', channel='1')
        


    # Remote Controller Configuration 
    c0 = net.addController('c0', controller=RemoteController, ip='172.31.132.205', port=6653)
 
    net.propagationModel(model="logDistance", exp=3.6)
   
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    print "*** Associating Stations"
    #Hosting mesh network and associating nodes
    net.addLink(mpoint, cls=physicalMesh, intf='wlx8416f91916ac', ssid='mesh-ssid', channel=1)
    net.addLink(ap1, cls=mesh, intf='ap1-wlan2', ssid='mesh-ssid', channel=1)
    net.addLink(ap2, cls=mesh, intf='ap2-wlan2', ssid='mesh-ssid', channel=1)
    net.addLink(mr1, cls=mesh, intf='mr1-wlan0', ssid='mesh-ssid', channel=1)
    net.addLink(mr2, cls=mesh, intf='mr2-wlan0', ssid='mesh-ssid', channel=1)
    
    print """plotting graph"""
    net.plotGraph(max_x=400, max_y=400)
    
    print "*** Starting network"
    net.build()

    # Assign IP address to USB dongle mesh interface
    os.system('ip addr add 10.0.0.3/16 dev phympoint-mp0')

    # Add route in the root system for the other mesh network
    os.system('route add -net 10.0.2.0/24 gw 10.0.2.1 phympoint-mp0')
    os.system('route add -net 10.0.1.0/24 gw 10.0.1.1 phympoint-mp0')
    # Enable IP forwarding in mesh portal
    mpoint.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    
    # Add gateway entry in the nodes
    sta1.cmd('route add -net 10.0.0.0/16 gw 10.0.3.1')
    sta2.cmd('route add -net 10.0.0.0/16 gw 10.0.3.1')
    sta3.cmd('route add -net 10.0.0.0/16 gw 10.0.3.1')
    sta4.cmd('route add -net 10.0.0.0/16 gw 10.0.3.1')
    mr1.cmd('route add -net 10.0.0.0/16 gw 10.0.3.1')
    mr2.cmd('route add -net 10.0.0.0/16 gw 10.0.3.1')

    # Start controller and Openflow enabled mesh access points
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    
 
    info("*** Running CLI\n")
    CLI_wifi(net)

    # Delete the mesh interface created previously
    os.system('iw dev phympoint-mp0 del')

    print "*** Stopping network"
    net.stop()
    os.system('mn -c')
    os.system('pkill -9 python3')    

if __name__ == '__main__':
    setLogLevel('info')
    topology()
