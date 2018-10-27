from conn_api import init_logging, threads_conn, connect_ssh
from conn_app import open_excel_file, router_params


print('Insert command for send to routers')
command = input('Command:')


file = 'routers_1.xlsx'
init_logging('movie-app.log')
routers_parameter = open_excel_file(file)
router = router_params(routers_parameter)
all_done = threads_conn(connect_ssh, router, command)
print(all_done)
