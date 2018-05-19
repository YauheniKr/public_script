from pprint import pprint
from netmiko import ConnectHandler
import getpass
import openpyxl
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

def connect_ssh(device_dict, command):
    print('Connection to device: {}'.format(device_dict['ip']))
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
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices, repeat(command))
    return list(f_result)



device_dict_list = []
device_template = ['ip', 'device_type', 'username', 'password', 'secret']


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