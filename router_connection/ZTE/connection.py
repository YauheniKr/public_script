from conn_api import init_logging, threads_conn, connect_ssh
from conn_app import open_excel_file, router_params, take_command_line, input_credentials
from conn_app import parser_show_clitable
from tabulate import tabulate

file = 'routers_1.xlsx'

def main():
    init_logging('movie-app.log')
    routers_parameter = open_excel_file(file)
    router = router_params(routers_parameter)
    inf = threads_conn(connect_ssh, router)
    all_done = parser_show_clitable(''.join(list(inf.values())), router)
    print(f'')
    print(tabulate(all_done, headers = all_done[0], tablefmt = 'grid', stralign='center'))

if __name__ == '__main__':
    main()