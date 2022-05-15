from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.ssh_exception import NetmikoAuthenticationException
import threading
import os


def config_worker(username, password, device):
    try:
        dev_dict = {
            'username': username,
            'password': password,
            'ip': device,
            'device_type': 'cisco_ios'
        }
        session = ConnectHandler(**dev_dict)
        print('--- logged in to device ', device)
        file_path = 'input/'+str(device)+'.cfg'
        with open (file_path, 'r') as f:
            commands = f.read().splitlines()
        output = session.send_config_set(commands)
        with open ('output/configuration/'+device+'.txt', 'a+') as f:
            f.write(output)
        return

    except NetmikoAuthenticationException:
        print ("Cannot reach the device", device)
    except NetmikoAuthenticationException:
        print ("Invalid Credentials on device", device)
        


def main ():
    dev_list = ['router1', 'router2', 'router3', 'router4']
    config_thread_list = []
    username = os.getenv('GNS3_UNAME')
    password = os.getenv('GNS3_PASS')
    for device in dev_list:
        config_thread_list.append(threading.Thread(target=config_worker, args=(username, password, device)))
    for config_thread in config_thread_list:
        config_thread.start()
    for config_thread in config_thread_list:
        config_thread.join()


if __name__ == "__main__":
    main()
