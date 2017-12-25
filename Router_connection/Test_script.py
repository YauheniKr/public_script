import openpyxl
import sys
import getpass


def open_excel_routers(file):
    addresses = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.get_active_sheet()
    for row in range(1, sheet.max_row+1):
        addresses.append(sheet['A'+str(row)].value)
    return addresses

def device_template(device_list, device_template):
    device_temp = dict.fromkey(device_template)
    for key in list(device_temp.keys()):
        device


def send_show_command(device_list, command):
    key=[]
    result_comm_dict={}
    for dict in device_list:
        key = list(dict.keys())
        print('Подключаемся к устройству с IP адресом {} '.format(dict[key[1]]))
        with ConnectHandler(**dict) as ssh:
            ssh.enable()
            result_comm = ssh.send_command(command)
            print(result_comm)
            result_comm_dict[dict[key[1]]]=result_comm
    #print(result_comm_dict)
    return(result_comm_dict)

device_list = []
device = []
device_template = ['device_type', 'ip', 'username', 'password', 'enable']

print('Insert Username, Password and device type for connection')
Username = input('Username:')
Password = getpass.getpass()
enable_Password = Password
device_type = input('Device Type(cisco_ios for ssh or cisco_ios_telnet for telnet ):')
device.append(device_type)

file = sys.argv[1]
test = open_excel_routers(file)
for address in test:
    device.append(address)
    device = device + Username.split() + Password.split() + enable_Password.split()
    device_list.append(device)
    device = []
print(device_list)
