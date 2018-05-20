from pprint import pprint
from netmiko import ConnectHandler
from datetime import datetime
import getpass
import openpyxl
import netmiko.ssh_exception
from concurrent.futures import ThreadPoolExecutor, as_completed


def connect_ssh(device_dict, command):
    print('Connection to device: {} \n'.format(device_dict['ip']))
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return {device_dict['ip']: result}


def open_excel_routers(file):
    addresses = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    for row in range(1, sheet.max_row+1):
        addresses.append(sheet['A'+str(row)].value)
    return addresses


def threads_conn(function, devices, command, limit=2):
    all_results = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command) for device in devices]
        for f in as_completed(future_ssh):
            try:
                result = f.result()
            except netmiko.ssh_exception.NetMikoAuthenticationException as e:
                print(e)
                break
            except netmiko.ssh_exception.NetMikoTimeoutException as e:
                print(e)
            else:
                all_results.update(result)
        for f in reversed(future_ssh):
            if not f.cancel():
                try:
                    all_results.update(f.result())
                except netmiko.ssh_exception.SSHException:
                    pass
    return all_results



device_dict_list = []
device_template = ['ip', 'device_type', 'username', 'password', 'secret']

start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'


Username = input('Username:')
Password = getpass.getpass()
print('Insert command for send to routers')
command = input('Command:')
device_type = input('Device type:')
device_values_kn = [device_type, Username, Password, Password]
#file = input('Filename:')
dict_values = []
file = 'routers.xlsx'
routers = open_excel_routers(file)

for ip in routers:
    device_values = []
    device_values.append(ip)
    device_values.extend(device_values_kn)
    device_dict_main = {k: v for (k, v) in zip(device_template, device_values)}
    device_dict_list.append(device_dict_main)

all_done = threads_conn(connect_ssh, device_dict_list, command)
pprint(all_done)