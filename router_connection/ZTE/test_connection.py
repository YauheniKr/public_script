import netmiko
import getpass
import openpyxl

class CiscoSSH:
    def __init__(self, *args):
        device_params_key = ['username', 'password', 'secret', 'ip']
        device_params = {key:value for (key, value) in zip(device_params_key, args)}
        device_params.update({'device_type': 'cisco_ios'})
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()

    def send_show_command(self, command):
        return self.ssh.send_command(command)

def open_excel_routers(file):
    addresses = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    for row in range(1, sheet.max_row+1):
        addresses.append(sheet['A'+str(row)].value)
    return addresses


Username = input('Username:')
Password = getpass.getpass()
print('Insert command for send to routers')
command = input('Command:')
device_type = input('Device type:')
file = input('Filename:')
routers = open_excel_routers(file)
print(routers)