import ipaddress
import os
import socket
import struct
import sys


class IP:

        def __init__(self,buff=None):
                header = struct.unpack('<BBHHHBBH4s4s', buff)
                self.ver = header[0] >> 4
                self.ihl = header[0] & 0xF

                self.tos = header[1]
                self.len = header[2]
                self.id = header[3]
                self.offset = header[4]
                self.ttl = header[5]
                self.protocol_num = header[6]
                self.sum = header[7]
                self.src = header[8]
                self.dst = header[9]

                # human readable IP addresses
                self.src_address = ipaddress.ip_address(self.src)
                self.dst_address = ipaddress.ip_address(self.dst)

                # map protocol constants to their name
                self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

                try:
                        self.protocol = self.protocol_map[self.protocol_num]
                except Exception as e:
                        print('%s No prortocol for %s' %(e, self.protocol_num))
                        self.protocol = str(self.protocol_num)

class ICMP:
	def __init__(self, buff):
		header = struct.unpack('<BBHHH', buff)
		self.type = header[0]
		self.code = header[1]
		self.sum = header[2]
		self.id = header[3]
		self.seq = header[4]

def sniff(host):
	# should look familiar from previous example
	if os.name == 'nt':
		socket_protocol = socket.IPPROTO_IP
	else:
		socket_protocol = socket.IPPROTO_ICMP
		sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
		sniffer.bind((host, 0))
		sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

		if os.name == 'nt':
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

		try:
			while True:
			# read a packet
				raw_buffer = sniffer.recvfrom(65535)[0]
				# create an IP header from the first 20 bytes
				ip_header = IP(raw_buffer[0:20])
				# print the detected protocl and hosts 
				print('Protocol: %s %s -> %s' %(ip_header.protocol, ip_header.src_address, ip_header.dst_address))



				ip_header = IP(raw_buffer[0:20])
				# if it's ICMP, we want it
				if ip_header.protocol == "ICMP":
					print('Protocol: %s %s -> %s' %(ip_header.protocol, ip_header.src_address, ip_header.dst_address))
					print(f'Version: {ip_header.ver}')
					print(f'Header Length: {ip_header.ihl} TTL: {ip_header.ttl}')
					# calculate where our ICMP packet starts
					offset = ip_header.ihl * 4
					buf = raw_buffer[offset:offset + 8]
					# create our ICMP structure
					icmp_header = ICMP(buf)
					print('ICMP -> Type: %s code: %s\n' %(icmp_header.type, icmp_header.code))
		except KeyboardInterrupt:
			if os.name == 'nt':
				sniffer.ioctl(socket.SIO_RCVALL, socket.RCV_OFF)
		sys.exit()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		host = sys.argv[1]
	else:
		host = '192.168.80.174'
	sniff(host)




"""
Exmaple Input & Output
Input:
└─$ ping www.google.com
PING www.google.com (142.250.67.164) 56(84) bytes of data.
64 bytes from bom12s07-in-f4.1e100.net (142.250.67.164): icmp_seq=1 ttl=128 time=20.6 ms
64 bytes from bom12s07-in-f4.1e100.net (142.250.67.164): icmp_seq=2 ttl=128 time=41.9 ms
64 bytes from bom12s07-in-f4.1e100.net (142.250.67.164): icmp_seq=3 ttl=128 time=17.3 ms
Output:
└─$ sudo python3 sniffer_with_icmp.py
Protocol: ICMP 142.250.67.164 -> 192.168.80.174
Protocol: ICMP 142.250.67.164 -> 192.168.80.174
Version: 4
Header Length: 5 TTL: 128
ICMP -> Type: 0 code: 0
Protocol: ICMP 142.250.67.164 -> 192.168.80.174
Protocol: ICMP 142.250.67.164 -> 192.168.80.174
Version: 4
Header Length: 5 TTL: 128
ICMP -> Type: 0 code: 0
"""
