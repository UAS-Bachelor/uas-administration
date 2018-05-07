from util import configobj, run_test


def run():
    for service_section in configobj:
        run_test(service_section)


if __name__ == '__main__':
    run()
