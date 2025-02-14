from application.setup import setup
from presentation.flet.ui import build


def main():
    t_service, a_service = setup()
    # cli = ClickCLI(t_service, a_service)
    # cli.start()

    build(t_service, a_service)


if __name__ == '__main__':
    main()
