from netmiko import ConnectHandler
import os
import time
import threading


def config_worker (host, password):
    dev_info = {
        'ip': host,
        'username': 'nanda',
        'password': password,
        'device_type' : 'cisco_ios'
    }
    session = ConnectHandler(**dev_info)
    output = session.send_command('show version')
    print(output)


start_time = time.time()
password = input('Enter the password: ')
config_threads_list = []
devices = ['r1' ,'r2', 'r3', 'r4']
for host in devices:
    config_threads_list.append(threading.Thread(target=config_worker, args = (host, password)))

for config_thread in config_threads_list:
    config_thread.start()

for config_thread in config_threads_list:
    config_thread.join()

print ('processing time', time.time()-start_time)
#3.204464912414551
#2.853083848953247