from napalm import get_network_driver
import threading
import os
import json

def config_worker(username, password, hostname):
    driver = get_network_driver('ios')
    device = driver(hostname, username, password)
    device.open()
#    output = device.get_facts()
#    print(json.dumps(output, indent=4))
    print('Connected to device', hostname)
    file_path = hostname+'.cfg'
    device.load_merge_candidate(filename= file_path)    
    delta = device.compare_config()
    if len(delta)>0:
        print('Delta on device', hostname)
        print (delta)
        print('Commiting the configuration on device', hostname)
        print ('\n')
        print ('\n')
        device.commit_config()
    else:
        print ('Delta is zero. No changes required on device', hostname, '\n')
        device.discard_config()
    device.close()

    return



def main ():
    dev_list = ['router1', 'router2', 'router3', 'router4']
    config_thread_list = []
    username = os.getenv('GNS3_UNAME')
    password = os.getenv('GNS3_PASS')
    for hostname in dev_list:
        config_thread_list.append(threading.Thread(target=config_worker, args=(username, password, hostname)))
    for config_thread in config_thread_list:
        config_thread.start()
    for config_thread in config_thread_list:
        config_thread.join()


if __name__ == "__main__":
    main()