import openpyxl
from datetime import datetime
import netaddr


def open_excel_routers(file):
    wb = openpyxl.load_workbook(file)
    for sheet_name in wb.sheetnames[1:]:
        addresses = []
        sheet = wb[sheet_name]
        for row in sheet.iter_rows():
            for cells in row:
                addresses.append(cells.value)
        yield addresses

def get_excel_sheets(file):
    wb = openpyxl.load_workbook(file)
    return wb.sheetnames[1:]

def save_output_to_excel(output_list, file_name, sheet_name):
    from openpyxl import Workbook
    wb = Workbook()
    for position, sheetname in enumerate(sheet_name, 0):
        sheet = wb.create_sheet(sheetname, position)
    for i in range(0, len(output_list)):
        sheet = wb[sheet_name]
        #for k in range(0, len(output_list[i])):
        sheet.cell(row=output_list.index(output_list[i])+1, column=(1)).value = output_list[i]
    wb.save(file_name)


list_network_full = []
file_name = 'output_aggr.xlsx'
opcos_address = open_excel_routers('список публичных префиксов.xlsx')
sheet_name = get_excel_sheets('список публичных префиксов.xlsx')
for position, address in enumerate(opcos_address):
    #print(address)
    #print(sorted(address))
    list_netw_aggr = netaddr.cidr_merge(address)
    list_network = [str(network) for network in list_netw_aggr]
#print(list_network_full)
    save_output_to_excel(list_network, file_name, sheet_name[position])
