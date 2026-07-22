from parts.chassis import Chassis
from core.export import export


def main():

    chassis = Chassis().build()

    export("chassis", chassis)


if __name__ == "__main__":
    main()