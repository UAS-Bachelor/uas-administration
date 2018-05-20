from util import configobj, run_test


def run():
    print("Running tests in: ")
    for service_section in configobj:
        if configobj[service_section].as_bool('hasTests'):
            print("- " + service_section + " module")
            run_test(service_section)


if __name__ == '__main__':
    run()
