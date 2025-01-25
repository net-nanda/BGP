from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from netmiko import ConnectHandler, NetmikoTimeoutException
import os
import json
from json.decoder import JSONDecodeError
import time
from paramiko.ssh_exception import SSHException

def config_worker(device):
    try:    
        login_info = {
            'ip': device,
            'username': os.getenv('NET_USER'),
            'password': os.getenv('NET_PASS'),
            'device_type': 'juniper_junos'
        }
        session = ConnectHandler(**login_info)
        output = session.send_command('show version|display json')
        output = json.loads(output)
        hostname = output["software-information"][0]["host-name"][0]['data']
        model = output["software-information"][0]["product-model"][0]['data']
        version = output["software-information"][0]["junos-version"][0]['data']
        device_details = {
            'Hostname': hostname,
            'Model': model,
            'Version': version
        }
        device_data.append(device_details)
    except NetmikoTimeoutException:
        print(f"IP unreachable {device}")
    except JSONDecodeError:
        print(f"JSON Decode Error on {device}")
    except SSHException:
        print (f"Banner Error on {device}")

start_time = time.time()
os.system('rm dev_inventory.csv && rm DEV1_INVENTORY.csv')
device_data = []
dev_list = [f"10.255.255.{i}" for i in range(1,256) ]

with ThreadPoolExecutor(max_workers=256) as executor:
    executor.map(config_worker, dev_list)

df = pd.DataFrame(device_data)
output_file = 'dev_inventory.csv'
df.to_csv(output_file, index=False)
os.system('(head -n 1 dev_inventory.csv&& tail -n +2 dev_inventory.csv| sort -k1 ) >> DEV1_INVENTORY.csv')
print(f'Execution time: {time.time()-start_time}')