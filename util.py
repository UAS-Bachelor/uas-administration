from configobj import ConfigObj
from sys import executable
from subprocess import Popen
import psutil

__services_dir = 'services/'
__services_config = 'services.ini'
configobj = ConfigObj(__services_config)


def __get_path(service):
    return __services_dir + service + '/' + service + '.py'


def __get_test_path(service):
    return __services_dir + service + '/test_suite.py'


def open_cmd(service, port, version):
    Popen([executable, __get_path(service), '-p', str(port),
           '-v', str(version)])


def run_test(service):
    Popen([executable, __get_test_path(service)])


def close_cmd(pid):
    psutil.Process(pid).terminate()


def check_port(port_to_check):
    amount_of_instances = 0
    for connection in psutil.net_connections('inet'):
        (ip, port) = connection.laddr
        if ip == '127.0.0.1' and port == int(port_to_check):
            amount_of_instances += 1
    return amount_of_instances


def gather_pids(port_to_check):
    pids = []
    for connection in psutil.net_connections('inet'):
        (ip, port) = connection.laddr
        if ip == '127.0.0.1' and port == int(port_to_check) and connection.pid != 0:
            pids.append(connection.pid)
    return pids
