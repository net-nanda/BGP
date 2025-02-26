from netmiko import ConnectHandler
import pandas as pd
import os 
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Environment, FileSystemLoader
import ipaddress

def get_vars (dev_vars):
    dev_dict = {
        's0_0' : ipaddress.IPv4Interface(dev_vars['s0_0']).ip,
        's0_1' : ipaddress.IPv4Interface(dev_vars['s0_1']).ip,
        'lo0' : ipaddress.IPv4Interface(dev_vars['lo0']).ip,
        'lo1' : ipaddress.IPv4Interface(dev_vars['lo1']).ip,
        'lo2' : ipaddress.IPv4Interface(dev_vars['lo2']).ip,
        'lo3' : ipaddress.IPv4Interface(dev_vars['lo3']).ip,
        'wan_mask' : ipaddress.IPv4Interface(dev_vars['s0_0']).netmask,
        'lan_mask' : ipaddress.IPv4Interface(dev_vars['lo3']).netmask,
        'wan_net1' : ipaddress.IPv4Interface(dev_vars['s0_0']).network[0],
        'wan_net2' : ipaddress.IPv4Interface(dev_vars['s0_1']).network[0],
        'lo0_net' : ipaddress.IPv4Interface(dev_vars['lo0']).network[0],
        'lo1_net' : ipaddress.IPv4Interface(dev_vars['lo1']).network[0],
        'lo2_net' : ipaddress.IPv4Interface(dev_vars['lo2']).network[0],
        'lo3_net' : ipaddress.IPv4Interface(dev_vars['lo3']).network[0],
        'asn' : dev_vars['asn']
    }
    return dev_dict

def config_worker(dev_list):
    df = pd.read_csv('../base_topology_data.csv')
    row = df[df['hostname'] == dev_list] 
    dev_vars = row.to_dict(orient='records')[0]
    dev_dict = get_vars(dev_vars)
    ENV = Environment(loader=FileSystemLoader('../jinja_templates'))
    int_config_tmp = ENV.get_template('base_topology_config.j2')
    int_config = int_config_tmp.render(dev_vars=dev_dict)
    login_info = {
        'ip': dev_list,
        'username': os.getenv('DEV_ADMIN'),
        'password': os.getenv('DEV_KEY'), 
        'device_type': 'cisco_ios'
    } 
    # session = ConnectHandler(**login_info)
    # output = session.send_config_set(int_config)
    # print(output)
    bgp_config_tmp = ENV.get_template(dev_list+'_bgp.j2')
    data = df.to_dict(orient='records')
    for row in data:
        if row['hostname'] == 'r1':
            r1_dict = get_vars(row)
        if row['hostname'] == 'r2':
            r2_dict = get_vars(row)
        if row['hostname'] == 'r3':
            r3_dict = get_vars(row)
        if row['hostname'] == 'r4':
            r4_dict = get_vars(row) 
    bgp_config = bgp_config_tmp.render(r1_dict=r1_dict, r2_dict=r2_dict, r3_dict=r3_dict,r4_dict=r4_dict)
    print('#'*5+' loggin to device '+dev_list+' #'*5)
    session = ConnectHandler(**login_info)
    output = session.send_config_set(bgp_config)
    print(output)
    print('#'*20)
    return

dev_list = ['r1', 'r2', 'r3', 'r4']
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(config_worker, dev_list)
