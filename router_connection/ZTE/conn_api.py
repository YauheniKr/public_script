from netmiko import ConnectHandler
import netmiko.ssh_exception
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import logbook


app_log = logbook.Logger('App')


class RouterSSH:
    def __init__(self, **device_dict):
        self.device_dict = device_dict
        self.ssh = ConnectHandler(**device_dict)

    def send_command(self, command):
        app_log.trace('Send command {} to device {} \n'
                      .format(command, self.device_dict['ip']))
        if not self.ssh.check_enable_mode:
            self.ssh.enable()
        return self.ssh.send_command(command, strip_prompt=False)

    def send_config_commands(self, commands, file=None):
        app_log.trace('Send command {} to device {} \n'
                      .format(commands, self.device_dict['ip']))
        self.ssh.send_config_from_file(config_file=file, **kwargs)
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        print('Закрываю соединение с устройством: {} \n'
              .format(self.device_dict['ip']))
        app_log.trace('Закрываю соединение с устройством: {} \n'
                      .format(self.device_dict['ip']))
        self.ssh.disconnect()


def connect_ssh(device_dict, command, ):
    app_log.trace('Connection to device: {}'.format(device_dict['ip']))
    print('Connection to device: {}'.format(device_dict['ip']))
    with RouterSSH(**device_dict) as session:
        result = session.send_command(command)
    return {device_dict['ip']: result}


def threads_conn(function, devices, command, limit=2):
    all_results = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(function, device, command)
                      for device in devices]
        for f in as_completed(future_ssh):
            try:
                result = f.result()
            except netmiko.ssh_exception.NetMikoAuthenticationException as e:
                app_log.trace(e)
                print(e)
                break
            except netmiko.ssh_exception.NetMikoTimeoutException as e:
                app_log.trace(e)
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


def init_logging(filename: str = None):
    level = logbook.TRACE
    if filename:
        logbook.TimedRotatingFileHandler(filename, level=level)\
            .push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()
    msg = 'Logging initialized, level: {}, mode: {}'.format(
        level,
        "stdout mode" if not filename else 'file mode: ' + filename
    )
    logger = logbook.Logger('Startup')
    logger.notice(msg)
