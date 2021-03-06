import openpyxl
import sys
import getpass
import telnetlib
import time
import re
from tabulate import tabulate


def open_excel_routers(filename):
    addresses = []
    wb = openpyxl.load_workbook(filename)
    sheet = wb.get_active_sheet()
    for row in range(1, sheet.max_row+1):
        addresses.append(sheet['A'+str(row)].value)
    return addresses


"""
def device_dict(device_list, device_template):
    device_dict_list = []
    for dev in device_list:
        device_dic = dict.fromkeys(device_template)
        for key in list(device_dic.keys()):
            device_dic[key] = dev[(device_template.index(key))]
            device_dict_list.append(device_dic)
    return device_dict_list
"""


def parser_show_interface_description(output, template_file):
    import textfsm
    result = []
    f = open(template_file)
    re_table = textfsm.TextFSM(f)
    result_header = re_table.header
    result.append(result_header)
    result_output = re_table.ParseText(output)
    result.extend(result_output)
    return result


"""
def send_show_command(device_list, command):
    key=[]
    result_comm_dict={}
    for dict in device_list:
        key = list(dict.keys())
        print('Подключаемся к устройству с IP адресом {} '.format(dict[key[1]]))
        with ConnectHandler(**dict) as telnet:
            telnet.enable()
            result_comm = telnet.send_command(command)
            print(result_comm)
            result_comm_dict[dict[key[1]]]=result_comm
    #print(result_comm_dict)
    return(result_comm_dict)
"""


def send_show_command(address_list, command, Username, Password):
    output_list = []
    for IP in address_list:
        print('Connection to device {}'.format(IP))
        with telnetlib.Telnet(IP) as t:
            t.read_until(b'Username:')
            t.write(Username + b'\n')

            t.read_until(b'Password:')
            t.write(Password + b'\n')
            #t.write(b'enable\n')

            #t.read_until(b'Password:')
            #t.write(ENABLE_PASS + b'\n')
            t.write(b'terminal length 0\n')
            t.write(command + b'\n')

            time.sleep(5)

            output = t.read_very_eager().decode('utf-8')
            output_list.append(output.strip())
    return output_list


device_list = []
device = []
device_template = ['device_type', 'ip', 'username', 'password', 'enable']
#command = 'show mac table'.encode('utf-8')

print('Insert Username and Password')
Username = input('Username:').encode('utf-8')
Password = getpass.getpass().encode('utf-8')
print('Insert command for send to routers')
command = input('Command:').encode('utf-8')
#enable_Password = Password
#device_type = input('Device Type(cisco_ios for ssh or cisco_ios_telnet for telnet ):')
#device.append(device_type)

template = 'template.txt'
file = sys.argv[1]
address_list = open_excel_routers(file)
"""
for address in address_list:
    device.append(address)
    device = device + Username.split() + Password.split() #+ enable_Password.split()
    device_list.append(device)
    #device = []
device_list = device_dict(device_list, device_template)
#command_listing = send_show_command(device_list, command)
"""
output_command = send_show_command(address_list, command, Username, Password)
output_command_cleared = re.sub('(\r\n {66})', '', ''.join(output_command))
listing = parser_show_interface_description(output_command_cleared, template)
print(tabulate(listing[1:], headers=listing[0]))
