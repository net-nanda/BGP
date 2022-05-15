from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.ssh_exception import NetmikoAuthenticationException
import threading
import os


def config_worker(username, password, device):
    print ('---- logging to device ', device)
    try:
        dev_dict = {
            'username': username,
            'password': password,
            'ip': device,
            'device_type': 'cisco_ios',
            'fast_cli': False
        }
        session = ConnectHandler(**dev_dict)
        command_file = 'input/'+device+'.txt'
        with open(command_file, 'r') as f:
            command_list = f.read().splitlines()
        for command in command_list:
            output = session.send_command(command, read_timeout=60)
            print(output)
            with open('output/pre_validation/'+device+'.txt', 'a+') as f:
                string1 = "--- "+command+" ---\n"
                f.write(string1)
                f.write(output)
                f.write('\n')
                f.write('\n')
                f.write('\n')
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
