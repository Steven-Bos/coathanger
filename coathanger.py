import logging
import paramiko
import sys
import time
import getpass

if len(sys.argv) < 2:
    print('USAGE: HOST USERNAME')
    sys.exit()
 
# Host to connect to
HOST = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = str(getpass.getpass(prompt="Enter your password: "))
# Initiate SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
# Loop until authentication was successful
try:
    print('Trying to authenticate...')
    client.connect(
        HOST,
        port=22,
        username=USERNAME,
        password=PASSWORD,
        banner_timeout=5,
        timeout=15
    )

# Handle authentication failure exception
except paramiko.AuthenticationException:
    print('Authentication failed! Retrying...')
    sys.exit(),

except paramiko.SSHException:
    print('Unknown SSH error! Retrying...')
    sys.exit(),

print('Authentication successful!')
 
try:
    print('Trying to invoke a shell...')
    channel = client.invoke_shell()
 
except paramiko.SSHException:
    print('Unknown SSH error! Exiting.')
    sys.exit(),

# print('Setting context to Global')
# channel.send(str.encode('config global\n'))
# while not channel.recv_ready():
#     time.sleep(2)
# output = channel.recv(9999)
# print(output.decode())

print('Getting PIDs from https.')
channel.send(str.encode('diagnose sys process pidof httpsd\n'))
while not channel.recv_ready():
    time.sleep(2)
output = channel.recv(9999)
print(output.decode())

PIDs = output.decode().split('\n')
for PID in PIDs[1:-2]:
    myPID = str(PID).rstrip("\r")
    print('Getting GID for PID:' + myPID)
    command = 'diagnose sys process dump ' + myPID + ' | grep Gid\n'
    channel.send(str.encode(command))
    while not channel.recv_ready():
        time.sleep(2)
    output = channel.recv(9999)
    print(output.decode())

channel.close()