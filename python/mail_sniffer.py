from scapy.all import sniff

def packet_callback(packet):
	print(packet.show())

def main():
	sniff(prn = packet_callback, count=1)

if __name__ == '__main__':
	main()


"""
Output
└─$ sudo python3 mail_sniffer.py                                                                                                                                                        1 ⨯
###[ Ethernet ]### 
  dst       = 00:50:56:fd:1c:df
  src       = 00:0c:29:12:ba:9e
  type      = IPv4
###[ IP ]### 
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 40
     id        = 3350
     flags     = DF
     frag      = 0
     ttl       = 64
     proto     = tcp
     chksum    = 0xd627
     src       = 192.168.80.174
     dst       = 142.250.183.65
     \options   \
###[ TCP ]### 
        sport     = 44626
        dport     = http
        seq       = 2673380542
        ack       = 736786663
        dataofs   = 5
        reserved  = 0
        flags     = A
        window    = 64239
        chksum    = 0x57ad
        urgptr    = 0
        options   = []
None
                               
"""
