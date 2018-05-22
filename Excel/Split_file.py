import openpyxl

def open_excel_routers(file):
    addresses = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    for row in range(1, sheet.max_row+1):
        addresses.append(sheet['A'+str(row)].value)
    return addresses

file1 = 'test.xlsx'
file2 = 'test_descr.xlsx'
f1 = open_excel_routers(file1)
f2 = open_excel_routers(file2)

print(f1)