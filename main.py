import utils.common as com
com.check()

import cli, services


def main():
    services.handler('init')
    cli.menu()


if __name__ == "__main__":
    main()
