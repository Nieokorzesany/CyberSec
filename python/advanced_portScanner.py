import optparse
from socket import *
from threading import *
import threading

def socket_scan(host,port):
    try:
        socket_connect = socket(AF_INET,SOCK_STREAM)
        socket_connect.settimeout(5)
        result=socket_connect.connect((host,port))
        print(f"[+] Port {port} otwarty")
    except Exception as exeption:
        print(f"[-] Port {port} zamkniety")
        print(f"[-] Powod: {str(exeption)}")
    finally:
        socket_connect.close()
    
def port_scanning(host,ports):
    try:
        ip = gethostbyname(host)
        print(f"[+] Skanowanie hosta {host}")
    except:
        print(f"[-] Nieznany host {host}")
        return
    for port in ports:
        t = Thread(target=socket_scan,args= (ip,int(port)))
        t.start()

def main():
    parser = optparse.OptionParser('socket_portScan ' + '-H <Host> -P <Port>')
    parser.add_option('-H', dest = 'host',type='string', help = 'skanowany host')
    parser.add_option('-P', dest = 'port',type='string',help = 'lista portow odzielonych przecinkami')
    (options,args) = parser.parse_args()
    host = options.host
    ports = str(options.port).split(',')
    if (host == None) | (ports[0] == None):
        print(parser.usage)
        exit(0)
    port_scanning(host,ports)

if __name__ =="__main__":
    main()
