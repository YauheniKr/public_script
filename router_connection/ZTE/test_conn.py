from conn_api import init_logging, threads_conn, connect_ssh
from conn_app import open_excel_file, router_params, take_command_line
from conn_app import parser_show_interface_description_clitable


#print('Insert command for send to routers')
#command = input('Command:')


file = 'routers_1.xlsx'
init_logging('movie-app.log')
routers_parameter = open_excel_file(file)
command = take_command_line()
router = router_params(routers_parameter)
inf = threads_conn(connect_ssh, router, command)
all_done = parser_show_clitable(''.join(list(inf.values())), command)
