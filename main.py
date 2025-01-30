from application.setup import setup
from presentation.cli.cli import ClickCLI


def main():
    t_service, a_service = setup()
    cli = ClickCLI(t_service, a_service)
    cli.start()


if __name__ == '__main__':
    main()
